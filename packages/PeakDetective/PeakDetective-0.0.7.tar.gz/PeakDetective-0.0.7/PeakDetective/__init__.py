from pyteomics import mzml
import sys
import numpy as np
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
from multiprocessing import Manager,Pool
from threading import Thread
from tensorflow import keras
from keras.constraints import max_norm
import keras.layers as layers
import scipy.stats as stats
from bisect import bisect_left
import math
import random as rd
import IPython.display
from copy import deepcopy
import sklearn.metrics as met
import pandas as pd


#Utility functions:
def startConcurrentTask(task,args,numCores,message,total,chunksize="none",verbose=True):

    if verbose:
        m = Manager()
        q = m.Queue()
        args = [a + [q] for a in args]
        t = Thread(target=updateProgress, args=(q, total, message))
        t.start()
    if numCores > 1:
        p = Pool(numCores)
        if chunksize == "none":
            res = p.starmap(task, args)
        else:
            res = p.starmap(task, args, chunksize=chunksize)
        p.close()
        p.join()
    else:
        res = [task(*a) for a in args]
    if verbose: t.join()
    return res

def safeNormalize(x):
    """
    Safely normalize a vector, x, to sum to 1.0. If x is the zero vector return the normalized unity vector
    """
    if np.sum(x) < 1e-6:
        tmp = np.ones(x.shape)
        return tmp / np.sum(tmp)
    else:
        return x/np.sum(x)

def normalizeMatrix(X):
    """
    Normalize a matrix so that the rows of X sum to one
    """
    return np.array([safeNormalize(x) for x in X])

def classify(preds):
    """
    Classify predictions, preds, by returning the index of the highest scoring class
    """
    classes = np.zeros(preds.shape)
    for x in range(len(preds)):
        classes[x,list(preds[x]).index(np.max(list(preds[x])))] = 1
    return classes


def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

def updateProgress(q, total,message = ""):
    """
    update progress bar
    """
    counter = 0
    while counter != total:
        if not q.empty():
            q.get()
            counter += 1
            #if counter % 20 == 0:
            printProgressBar(counter, total,prefix = message, printEnd="")


def getIndexOfClosestValue(l,v):
    """
    get index of list with closest value to v
    """
    order = list(range(len(l)))
    order.sort(key=lambda x:np.abs(l[x]-v))
    return order[0]

def generateSkylineFiles(peak_scores,peak_boundaries,samples,polarity,cutoff=0.0,frac=0.0,moleculeListName = "XCMS peaks"):
    transitionList = deepcopy(peak_scores)
    toDrop = []
    for index,row in transitionList.iterrows():
        if float(len([x for x in samples if row[x] > cutoff])) / len(samples) < frac:
            toDrop.append(index)

    transitionList = transitionList.drop(toDrop,axis=0)

    transitionList["Precursor Name"] = ["unknown " + str(index) for index, row in transitionList.iterrows()]
    transitionList["Explicit Retention Time"] = [row["rt"] for index, row in
                                                 transitionList.iterrows()]
    polMapper = {"Positive": 1, "Negative": -1}
    transitionList["Precursor Charge"] = [polMapper[polarity] for index, row in transitionList.iterrows()]
    transitionList["Precursor m/z"] = [row["mz"] for index,row in transitionList.iterrows()]
    transitionList["Molecule List Name"] = [moleculeListName for _ in range(len(transitionList))]
    transitionList = transitionList[
        ["Molecule List Name", "Precursor Name", "Precursor m/z", "Precursor Charge",
         "Explicit Retention Time"]]

    peakBoundariesSkyline = {}

    # iterate through filenames and cpds
    for fn in samples:
        for index, row in transitionList.iterrows():
            peakBoundariesSkyline[len(peakBoundariesSkyline)] = {"Min Start Time": peak_boundaries.at[index,fn][0],
                                                   "Max End Time": peak_boundaries.at[index,fn][1],
                                                   "Peptide Modified Sequence": row["Precursor Name"],
                                                   "File Name": fn}

    # format as df
    peakBoundariesSkyline = pd.DataFrame.from_dict(peakBoundariesSkyline, orient="index")
    peakBoundariesSkyline = peakBoundariesSkyline[["File Name", "Peptide Modified Sequence", "Min Start Time", "Max End Time"]]

    return transitionList,peakBoundariesSkyline





class PeakDetective():
    """
    Class for curation/detection of LC/MS peaks in untargerted metabolomics data
    """
    def __init__(self,resolution=100,numCores=1,windowSize = 1.0):
        self.resolution = resolution
        self.numCores = numCores
        self.windowSize = windowSize
        self.smoother = Smoother(resolution)
        self.classifier = Classifier(resolution)
        self.encoder = keras.Model(self.classifier.input, self.classifier.layers[6].output)

    def plot_overlayedEIC(self,rawdatas,mz,rt_start,rt_end,smoothing=0,alpha=0.3):
        ts = np.linspace(rt_start,rt_end,self.resolution)
        for data in rawdatas:
            s = data.interpolate_data(mz,rt_start,rt_end,smoothing)
            ints  = [np.max([x,0]) for x in s(ts)]
            plt.plot(ts,ints,alpha=alpha)


    @staticmethod
    def getNormalizedIntensityVector(data,mzs,rtstarts,rtends,smoothing,resolution,q=None):
        out = np.zeros((len(mzs),resolution))
        i=0
        for mz,rt_start,rt_end in zip(mzs,rtstarts,rtends):
            s = data.interpolate_data(mz,rt_start,rt_end,smoothing)
            out[i,:] = s(np.linspace(rt_start,rt_end,resolution))
            i += 1
        if type(q) != type(None):
            q.put(0)
        return out

    def makeDataMatrix(self,rawdatas,mzs,rtstarts,rtends,smoothing=0):
        args = []
        numToGetPerProcess = int(len(rawdatas)*len(mzs)/float(self.numCores))
        for rawdata in rawdatas:
            tmpMzs = []
            tmpRtStarts = []
            tmpRTends = []
            for mz,rtstart,rtend in zip(mzs,rtstarts,rtends):
                tmpMzs.append(mz)
                tmpRtStarts.append(rtstart)
                tmpRTends.append(rtend)
                if len(tmpMzs) == numToGetPerProcess:
                    args.append([rawdata,tmpMzs,tmpRtStarts,tmpRTends,smoothing,self.resolution])
                    tmpMzs = []
                    tmpRtStarts = []
                    tmpRTends = []

            if len(tmpMzs) > 0: args.append([rawdata, tmpMzs, tmpRtStarts, tmpRTends, smoothing,self.resolution])

        result = startConcurrentTask(PeakDetective.getNormalizedIntensityVector, args, self.numCores, "forming matrix", len(args))
        return np.concatenate(result,axis=0)

    def generateGaussianPeaks(self,n, centerDist, numPeaksDist=(0,2), widthFactor=0.1, heightFactor=1):
        X_signal = np.zeros((n,self.resolution)) #self.generateNoisePeaks(X_norm, tics)
        switcher = list(range(len(centerDist)))
        for x, s in zip(range(len(X_signal)), np.random.random(len(X_signal))):
            if numPeaksDist[0] >= numPeaksDist[1]:
                numGuass = numPeaksDist[0]
            else:
                numGuass = np.random.randint(numPeaksDist[0], numPeaksDist[1])
            for _ in range(numGuass):
                ind = int(np.random.choice(switcher))
                X_signal[x] += heightFactor * stats.norm.pdf(np.linspace(0, 1, self.resolution),
                                     stats.uniform.rvs(centerDist[ind][0], centerDist[ind][1] - centerDist[ind][0]),
                                     widthFactor * s + .001)
            #if np.sum(tmp) > 0:
            #    tmp = (1 - s2n[x]) * tmp / np.sum(tmp)
        X_signal = normalizeMatrix(X_signal)

        return X_signal

    def generateFalsePeaks(self,peaks,raw_datas, n=None):
        if type(n) == type(None):
            n = len(peaks)

        peaks_rand = pd.DataFrame()
        peaks_rand["rt"] = rd.choices(list(peaks["rt"].values),k=n)
        peaks_rand["mz"] = rd.choices(list(peaks["mz"].values),k=n)

        X_noise = self.makeDataMatrix(raw_datas,peaks_rand["mz"].values,peaks_rand["rt"].values - self.windowSize/2,peaks_rand["rt"].values + self.windowSize/2)

        signal_tics = np.array([np.sum(x) for x in X_noise])

        X_signal = normalizeMatrix(X_noise)

        return X_signal, signal_tics

    def generateSignalPeaks(self,peaks,raw_datas,widthFactor = 0.1,s2nFactor=.2,heightFactor = 1,min_signal = 1000,n=None):
        if type(n) == type(None):
            n = len(peaks)
        X_noise_peaks,noise_tics = self.generateFalsePeaks(peaks,raw_datas,n=n)
        X_signal_peaks = self.generateGaussianPeaks(n*len(raw_datas),[[0.45,0.5],[0.5,0.55]],(1,1),widthFactor,heightFactor)

        s2n = s2nFactor * np.random.random(len(X_signal_peaks))
        s2nInv = 1 - s2n

        signal_tics = np.array([max([min_signal,t*(1/x-1)]) for t,x in zip(noise_tics,s2n)])

        X_noise = s2n[:, np.newaxis] * X_noise_peaks
        X_signal = s2nInv[:, np.newaxis] * X_signal_peaks

        X = X_noise + X_signal

        X = normalizeMatrix(X)

        signal_tics = np.add(signal_tics,noise_tics)

        return X,X_signal,signal_tics


    def curatePeaks(self,raw_datas,peaks,smooth_epochs = 10,class_epochs = 10,batch_size=64,validation_split=0.1,useSynthetic=True,numManualPerRound = 3,min_peaks = 100000,shift = .5,threshold=.5,alpha=0.05,noise=1000,autoClassify = True,inJupyter = True):

        #generate data matrix
        print("generating EICs...")
        mzs = list(peaks["mz"].values)
        rt_starts = [row["rt"] - self.windowSize/2 for _,row in peaks.iterrows()]
        rt_ends = [row["rt"] + self.windowSize/2 for _,row in peaks.iterrows()]
        realEnd = len(mzs)


        if 2 * len(peaks) * len(raw_datas) < min_peaks:
            numToGet = int((min_peaks - 2 * len(peaks) * len(raw_datas))/len(raw_datas))
            print("insufficent # of EICs, shifting",numToGet,"random peaks", 0 , "to", shift , "minutes")
            tmp = list(range(len(mzs)))
            tmp = rd.choices(tmp,k=numToGet)

            mzs += [mzs[x] for x in tmp]
            shifts = [rd.choice([-1,1]) * shift * np.random.random() for x in tmp]
            rt_starts += [rt_starts[x] + shift for x,shift in zip(tmp,shifts)]
            rt_ends += [rt_ends[x] + shift for x,shift in zip(tmp,shifts)]

        X = self.makeDataMatrix(raw_datas,mzs,rt_starts,rt_ends)
        X_norm_clean = deepcopy(X)

        if useSynthetic:
            #generate synthetic data
            print("generating synthetic data...",end="")
            X_signal,X_pure,signal_tics = self.generateSignalPeaks(peaks,raw_datas,n=int(len(peaks)/2))
            X_noise,noise_tics = self.generateFalsePeaks(peaks,raw_datas,n=int(len(peaks)/2))
            X_noise_pure = np.zeros(X_noise.shape)

            X = np.concatenate((X,X_signal,X_noise))
            X_norm_clean = np.concatenate((X,X_pure,X_noise_pure))

            print("done")



        #normalize matrix
        X_norm = normalizeMatrix(X)
        X_norm_clean = normalizeMatrix(X_norm_clean)
        apexInd = int(np.floor(X_norm.shape[1]/2))
        tics = np.log10(np.array([np.max([2, np.sum(x)]) for x in X]))
        #ticsApex = np.log10(np.array([np.max([2,x[apexInd]]) for x in X]))
        ticsApex = np.log10(np.array([np.max([2,integratePeak(x)]) for x in X]))


        noiseInds = []
        for x in range(len(tics)):
            if np.power(10,tics[x]) * np.max(X_norm[x]) < noise:
            #if np.power(10,tics[x]) < noise:
                noiseInds.append(x)


        X_norm_clean[noiseInds] = np.zeros(X_norm_clean[noiseInds].shape)


        #X_norm_with_noise = normalizeMatrix(X + np.random.normal(noise,noise/2,X.shape))

        print("done")

        #fit autoencoder
        print("fitting smoother...")
        smoother = Smoother(self.resolution)
        smoother.fit(X_norm, X_norm_clean, epochs=smooth_epochs, batch_size=batch_size, validation_split=validation_split,verbose=1)#,sample_weight=np.power(10,tics))
        #smoother.fit(X, X, epochs=smooth_epochs, batch_size=batch_size, validation_split=validation_split)
        self.smoother = smoother
        self.encoder = keras.Model(smoother.input, smoother.layers[7].output)
        print("done")

        indsToKeep = []
        start = 0
        rt_starts_tmp = []
        rt_ends_tmp =[]
        for _ in raw_datas:
            indsToKeep += list(range(start,start + realEnd))
            start += len(rt_ends)
            rt_starts_tmp += list(rt_starts[:realEnd])
            rt_ends_tmp += list(rt_ends[:realEnd])

        rt_starts = rt_starts_tmp
        rt_ends = rt_ends_tmp
        X_norm = X_norm[indsToKeep]
        X = X[indsToKeep]

        if useSynthetic:
            #generate synthetic data
            #print("generating synthetic data...",end="")
            #X_signal,signal_tics = self.generateSignalPeaks(peaks,raw_datas,n=int(len(peaks)/2))
            #X_noise,noise_tics = self.generateFalsePeaks(peaks,raw_datas,n=int(len(peaks)/2))

            # signal_tics = np.log10(np.array([np.max([2, signal_tics[x] * X_signal[x,apexInd]]) for x in range(len(X_signal))]))
            # noise_tics = np.log10(np.array([np.max([2, noise_tics[x] * X_noise[x,apexInd]]) for x in range(len(X_noise))]))

            signal_tics = np.log10(np.array([np.max([2, integratePeak(signal_tics[x] * X_signal[x])]) for x in range(len(X_signal))]))
            noise_tics = np.log10(np.array([np.max([2, integratePeak(noise_tics[x] * X_noise[x])]) for x in range(len(X_noise))]))


            #create merged matrices
            y = np.array([[.5,.5] for _ in X_norm] + [[1,0] for _ in X_noise] + [[0,1] for _ in X_signal])
            X_merge = np.concatenate((X_norm,X_noise,X_signal),axis=0)
            tic_merge = np.concatenate((ticsApex, noise_tics,signal_tics))
            #tic_merge = np.ones(tic_merge.shape)

            #smooth data
            X_smoothed = self.smoother.predict(X_merge)
            X_merge = self.encoder.predict(X_merge)

            X_smoothed = normalizeMatrix(X_smoothed)

            #record real and synthethic observations
            synInds = [x for x in range(len(y)) if y[x][1] < .25 or y[x][1] > .75]
            realInds = [x for x in range(len(y)) if y[x][1] > .25 and y[x][1] < .75]

            updatingInds = list(realInds)
            trainingInds = list(synInds)

            print("done")

        else:
            y = np.array([[.5,.5] for _ in X_norm])
            X_smoothed = self.smoother.predict(X_norm)
            X_smoothed = normalizeMatrix(X_smoothed)

            X_merge = self.encoder.predict(X_norm)
            tic_merge = deepcopy(ticsApex)

            updatingInds = list(range(len(X_norm)))
            trainingInds = []

            realInds = list(range(len(X_norm)))

        print("classifying noise peaks")

        noiseCount = 0
        for ind in realInds:
            if np.power(10,tic_merge[ind]) * np.max(X_norm[ind]) < noise:
            #if np.max(X_norm[ind]) < noise:
                y[ind] = [1,0]
                updatingInds.remove(ind)
                #trainingInds.append(ind)
                noiseCount += 1
        print("done...",noiseCount,"noise peaks found")
        print("classifying remaining peaks...")

        numRemaining = []
        doMore = True
        i = 0
        labeledInds = []
        first = True
        performance = []
        while doMore:
            if len(updatingInds) > 0:
                print("round " + str(i+1) + ": " + str(len(updatingInds)) + " unclassified features")
                numRemaining.append(len(updatingInds))

                entropies = [-1 * np.sum([yyy * np.log(yyy) for yyy in yy]) for yy in y[updatingInds]]
                order = list(range(len(updatingInds)))
                order.sort(key=lambda x: entropies[x],reverse=True)
                order = [updatingInds[x] for x in order]

                if len(order) < numManualPerRound:
                    numManualPerRound = len(order)

                for ind in order[:numManualPerRound]:
                    print(ind,len(X),len(X_smoothed),len(rt_starts),len(rt_ends),len(y))
                    val = self.labelPeak([X[ind],np.sum(X[ind]) * X_smoothed[ind]],rt_starts[ind],rt_ends[ind],inJupyter,y[ind][1])
                    y[ind,0] = 1-val
                    y[ind,1] = val

                    trainingInds.append(ind)
                    updatingInds.remove(ind)
                    labeledInds.append(ind)

                if autoClassify:
                    for ind in updatingInds:
                       if y[ind][1] > 1-alpha or y[ind][0] > 1-alpha:
                           y[ind:ind+1] = classify(y[ind:ind+1])
                           trainingInds.append(ind)
                           updatingInds.remove(ind)

                classifer = ClassifierLatent(X_merge.shape[1])

                cb = keras.callbacks.EarlyStopping(
                    monitor="val_loss",
                    min_delta=0,
                    patience=3,
                    verbose=1,
                    mode="auto",
                    baseline=None,
                    restore_best_weights=True,
                )

                #labeledInds = list(set(trainingInds).intersection(set(realInds)))

                if first:
                    valInds = deepcopy(labeledInds)
                    tmpTrainInds = [x for x in trainingInds if x not in valInds]
                    if len(tmpTrainInds) == 0:
                        tmpTrainInds = deepcopy(updatingInds)
                    first = False
                else:
                    # valInds = rd.sample(labeledInds,k=int(validation_split*len(labeledInds)))
                    tmpTrainInds = [x for x in trainingInds if x not in valInds]


                history = keras.callbacks.History()

                classifer.fit([X_merge[tmpTrainInds], tic_merge[tmpTrainInds]], y[tmpTrainInds], epochs=int(class_epochs),
                              batch_size=batch_size, validation_split=validation_split, verbose=1,callbacks=[cb,history],
                              validation_data=([X_merge[valInds], tic_merge[valInds]], y[valInds]))


                #print("val loss:",history.history["val_loss"][cb.best_epoch],"val_mean_absolute_error",history.history["val_mean_absolute_error"][cb.best_epoch])

                y[updatingInds] = classifer.predict([X_merge[updatingInds], tic_merge[updatingInds]])

                plt.figure()
                plt.hist(y[realInds,1],bins=20)
                plt.title("round" + str(i+1))
                plt.show()

                performance.append(history.history["val_mean_absolute_error"][cb.best_epoch])

                print(str(len(updatingInds)) + " unclassified features remaining")
                print("Continue with another iteration? (1=Yes, 0=No): ")
                tmp = float(input())
                while not validateInput(tmp):
                    print("invalid classification: ")
                    tmp = float(input())
                doMore = bool(tmp)
            else:
                doMore = False
            i += 1


        scores = classifer.predict([X_merge[realInds], tic_merge[realInds]])[:,1]

        print("done")

        self.classifier = classifer

        print("formatting output...",end="")

        X = X_merge[realInds]
        tics = tic_merge[realInds]

        peaks_curated = {raw.filename: [] for raw in raw_datas}
        peak_scores = deepcopy(peaks)
        peak_intensities = deepcopy(peaks)

        keys = []
        for raw in raw_datas:
            peak_scores[raw.filename] = np.zeros(len(peak_scores.index.values))
            peak_intensities[raw.filename] = np.zeros(len(peak_scores.index.values))
            for index in peaks.index.values:
                keys.append([raw.filename, index])

        for [file, index], score,intensity in zip(keys, y[realInds][:,1],tic_merge[realInds]):
            peak_scores.at[index,file] = score
            peak_intensities.at[index,file] = intensity
            if score > threshold:
                peaks_curated[file].append(index)
        peaks_curated = {file: peaks.loc[peaks_curated[file], :] for file in peaks_curated}



        return peaks_curated,X,X_norm,tics,scores,numRemaining,peak_scores,performance,peak_intensities

    def label_peaks(self,raw_data,peaks,inJupyter = True):
        rt_starts = [row["rt"] - self.windowSize/2 for _,row in peaks.iterrows()]
        rt_ends = [row["rt"] + self.windowSize/2 for _,row in peaks.iterrows()]
        y = []
        mat = self.makeDataMatrix([raw_data],peaks["mz"].values,rt_starts,rt_ends)
        count = 1
        for vec,rt_start,rt_end in zip(mat,rt_starts,rt_ends):
            y.append(self.labelPeak([vec],rt_start,rt_end,inJupyter,str(count) + "/" + str(len(mat))))
            count += 1
        peaks["classification"] = y
        return peaks

    def labelPeak(self,vecs,rt_start,rt_end,inJupyter,title=""):
        plt.figure()
        xs = np.linspace(rt_start, rt_end, len(vecs[0]))
        [plt.plot(xs, vec) for vec in vecs]
        plt.xlabel("time (arbitrary)")
        plt.ylabel("intensity")
        plt.title(title)
        plt.show()
        print("Enter classification (1=True Peak, 0=Artifact): ")
        val = input()
        while not validateInput(val):
            print("invalid classification: ")
            val = input()
        val = float(val)
        plt.close()
        if inJupyter:
            IPython.display.clear_output(wait=True)

        return val

    def roiDetection(self,rawdata,intensityCutuff=100,numDataPoints = 3):
        rts = rawdata.rts
        rois = [{"mz_mean":mz,"mzs":[mz],"extended":False,"count":1} for mz, i in rawdata.data[rts[0]].items() if i > intensityCutuff]
        rois.sort(key=lambda x:x["mz_mean"])

        def binarySearchROI(poss,query):

            pos = bisect_left([x["mz_mean"] for x in poss],query)

            if pos == len(poss):
                if 1e6 * np.abs(query-poss[-1]["mz_mean"]) / query < rawdata.ppm:
                    return True, pos - 1
                else:
                    return False, pos
            elif pos == 0:
                if 1e6 * np.abs(query-poss[0]["mz_mean"]) / query < rawdata.ppm:
                    return True, 0
                else:
                    return False, pos
            else:
                ldiff = 1e6 * np.abs(query - poss[pos-1]["mz_mean"]) / query
                rdiff = 1e6 * np.abs(query - poss[pos]["mz_mean"]) / query

                if ldiff < rdiff:
                    if ldiff < rawdata.ppm:
                        return True, pos - 1
                    else:
                        return False, pos
                else:
                    if rdiff < rawdata.ppm:
                        return True, pos
                    else:
                        return False, pos


        counter = 0
        for rt in rts[1:]:
            printProgressBar(counter, len(rts),prefix = "Detecting ROIs",suffix=str(len(rois)) + " ROIs found",printEnd="")
            counter += 1
            for mz, i in rawdata.data[rt].items():
                if i > intensityCutuff:
                    update,pos = binarySearchROI(rois,mz)
                    #print(update,len(rois),pos)
                    if update:
                        rois[pos]["mzs"].append(mz)
                        rois[pos]["mz_mean"] = np.mean(rois[pos]["mzs"])
                        rois[pos]["extended"] = True
                        rois[pos]["count"] += 1
                    else:
                        if pos != len(rois):
                            rois.insert(pos,{"mz_mean":mz,"mzs":[mz],"extended":True,"count":1})
                        else:
                            rois.append({"mz_mean":mz,"mzs":[mz],"extended":True,"count":1})
                #if not(all(rois[i]["mz_mean"] <= rois[i+1]["mz_mean"] for i in range(len(rois) - 1))):
                #   print("error")



            toKeep = []
            for x in range(len(rois)):
                if rois[x]["extended"] == True or rois[x]["count"] >= numDataPoints:
                    toKeep.append(x)

            rois = [rois[x] for x in toKeep]

            for x in range(len(rois)):
                rois[x]["extended"] = False


        rois = [x["mz_mean"] for x in rois]
        print()
        print(len(rois)," ROIs found")

        return rois

    # def plot_classifier_interpretation(self,numPer = 100):
    #     sal_image = np.zeros((100, self.resolution))
    #     for col in range(self.resolution):
    #         printProgressBar(col, self.resolution,prefix = "Building classification map",printEnd="")
    #         for row in range(100):
    #             X = np.random.random((numPer, self.resolution))
    #             X[:, col] = float(row) / 100 * np.ones(X[:, col].shape)
    #             tics = np.ones(numPer)
    #             otherCols = [x for x in range(X.shape[1]) if x != col]
    #             X[:, otherCols] = (1 - float(row) / 100) * X[:, otherCols] / X[:, otherCols].sum(axis=1)[:, np.newaxis]
    #             scores = self.classifier([X, tics])[:, 1]
    #             sal_image[row, col] = np.mean(scores)
    #     plt.imshow(sal_image)
    #     plt.xlabel("time")
    #     plt.ylabel("relative intensity")
    #     plt.colorbar(label="mean output score")
    #     return sal_image

    def detectPeaks(self,rawData,rois,cutoff=0.5,window=10,time=1.0,noiseCutoff=4):
        print("generating all EICs from ROIs...")
        peaks = []
        dt = time/self.resolution
        tmpRes = int(math.ceil((rawData.rts[-1] - rawData.rts[0] + time) / dt))
        rt_starts = [rawData.rts[0]-time/2 for _ in rois]
        rt_ends = [rawData.rts[-1]+time/2 for _ in rois]
        oldRes = int(self.resolution)
        self.resolution = tmpRes
        X_tot = self.makeDataMatrix([rawData],rois,rt_starts,rt_ends,0)
        self.resolution = oldRes

        numPoints = math.floor(float(tmpRes - self.resolution)/window)


        X = np.zeros((int(numPoints * len(rois)),self.resolution))

        counter = 0

        mzs = []
        rts = []

        for row in range(len(rois)):
            start = 0
            end = self.resolution
            rt = float(rawData.rts[0])
            for _ in range(numPoints):
                X[counter,:] = X_tot[row,start:end]
                counter += 1
                start += window
                end += window
                mzs.append(rois[row])
                rts.append(rt)
                rt += dt * window


        tics = np.log10(np.array([np.max([2,integratePeak(x)]) for x in X]))
        X = normalizeMatrix(X)
        print("done, ",len(X)," EICs generated")
        print("smoothing EICs...")
        #X = self.smoother.predict(X,verbose=1)
        X = self.encoder.predict(X,verbose=1)

        print("done")
        print("classifying peaks...")
        y = self.classifier.predict([X,tics],verbose=1)[:,1]
        print("done")
        for mz,rt,score,tic in zip(mzs,rts,y,tics):
            if score > cutoff and tic > noiseCutoff:
                peaks.append([mz,rt,score])

        if len(peaks) > 0:
            peaks = pd.DataFrame(data=np.array(peaks), columns=["mz", "rt","score"])
        else:
            peaks = pd.DataFrame(columns=["mz", "rt","score"])

        print(len(peaks)," peaks found")

        return peaks,X

    def getPeakBoundaries(self,X,samples,peakScores,cutoff,frac):
        peakBoundaries = pd.DataFrame(index=peakScores.index.values)
        i = 0
        toFill = []
        goodInds = [index for index,row in peakScores.iterrows() if float(len([x for x in samples if row[x] > cutoff])) / len(samples) > frac]
        for samp in samples:
            bounds = []
            for index,row in peakScores.iterrows():
                if index in goodInds:
                    if row[samp] > cutoff:
                        lb,rb = findPeakBoundaries(X[i])
                        actualRts = np.linspace(row["rt"]-self.windowSize/2,row["rt"]+self.windowSize/2,self.resolution)
                        bounds.append((actualRts[lb],actualRts[rb]))
                    else:
                        bounds.append((-1,-1))
                        toFill.append((index,samp))
                else:
                    bounds.append((-1, -1))
            peakBoundaries[samp] = deepcopy(bounds)

        peakBoundaries = peakBoundaries.loc[goodInds,:]
        for index,samp in toFill:
            widths = [x[1]-x[0] for x in peakBoundaries.loc[index,:] if x[0] > 0 and x[1] > 0]
            centers = [np.mean(x) for x in peakBoundaries.loc[index,:] if x[0] > 0 and x[1] > 0]
            peakBoundaries.at[index,samp] = (np.mean(centers) - np.mean(widths)/2,np.mean(centers) + np.mean(widths)/2 )

        return peakBoundaries


def validateInput(input):
    try:
        input = float(input)
        if input not in [0,1]:
            return False
        return True
    except:
        return False

class rawData():
    def __init__(self):
        self.data = {}
        self.type = "centroid"
        self.filename = ""

    def readRawDataFile(self,filename,ppm,type="centroid",samplename=None):
        """
         Read MS datafile

        :param filename: str, path to MS datafile
        """
        try:

            reader = mzml.read(filename.replace('"', ""))
            ms1Scans = {}
            for temp in reader:
                if temp['ms level'] == 1:
                    ms1Scans[temp["scanList"]["scan"][0]["scan start time"]] = {mz: i for mz, i in
                                                                                zip(temp["m/z array"],
                                                                                    temp["intensity array"])}
            reader.close()
            self.rts = list(ms1Scans.keys())
            self.rts.sort()
            self.data = ms1Scans
            self.type = type
            self.filename = filename
            self.ppm = ppm

        except:
            print(sys.exc_info())
            print(filename + " does not exist or is ill-formatted")


    def extractEIC(self,mz,rt_start,rt_end):
        width = self.ppm * mz / 1e6
        mz_start = mz - width
        mz_end = mz + width
        rts = [x for x in self.rts if x > rt_start and x < rt_end]
        intensity = [np.sum([i for mz,i in self.data[rt].items() if mz > mz_start and mz < mz_end]) for rt in rts]
        return rts,intensity

    def integrateTargets(self,transitionList):
        areas = []
        for index,row in transitionList.iterrows():
            rts,intensity = self.extractEIC(row["mz"],row["rt_start"],row["rt_end"])
            area = np.trapz(intensity,rts)
            areas.append(area)
        transitionList[self.filename] = areas
        return transitionList

    def interpolate_data(self,mz,rt_start,rt_end,smoothing=1):
        rts,intensity = self.extractEIC(mz,rt_start,rt_end)
        if len(rts) > 3:
            smoothing = smoothing * len(rts) * np.max(intensity)
            s = UnivariateSpline(rts,intensity,ext=1,s=smoothing)
        else:
            s = UnivariateSpline([0,5,10,15],[0,0,0,0],ext=1,s=smoothing)
        return s

def Smoother(resolution):
    # build autoencoder
    autoencoderInput = keras.Input(shape=(resolution,))
    x = layers.Reshape((resolution, 1))(autoencoderInput)

    kernelsize = 3
    stride = 1
    max_norm_value = 2.0

    x = layers.Conv1D(32, kernelsize, strides=stride, activation='relu', kernel_constraint=max_norm(max_norm_value),
                     kernel_initializer='he_uniform')(x)

    #x = layers.BatchNormalization()(x)

    x = layers.Conv1D(16, kernelsize, strides=stride, activation='relu', kernel_constraint=max_norm(max_norm_value),
                     kernel_initializer='he_uniform')(x)

    #x = layers.BatchNormalization()(x)

    x = layers.Conv1D(8, kernelsize, strides=stride, activation='relu', kernel_constraint=max_norm(max_norm_value),
                      kernel_initializer='he_uniform')(x)

    #x = layers.BatchNormalization()(x)

    x = layers.Conv1D(4, kernelsize, strides=stride, activation='relu', kernel_constraint=max_norm(max_norm_value),
                      kernel_initializer='he_uniform')(x)

    #x = layers.BatchNormalization()(x)

    x = layers.Flatten()(x)

    x = layers.Dense(5, activation="relu")(x)

    x = layers.Dense(int((resolution-8) * 4), activation="relu")(x)

    x = layers.Reshape((resolution-8, 4))(x)

    x = layers.Conv1DTranspose(8, kernelsize, strides=stride, activation='relu',
                               kernel_constraint=max_norm(max_norm_value), kernel_initializer='he_uniform')(x)

    #x = layers.BatchNormalization()(x)

    x = layers.Conv1DTranspose(16, kernelsize, strides=stride, activation='relu',
                              kernel_constraint=max_norm(max_norm_value), kernel_initializer='he_uniform')(x)

    #x = layers.BatchNormalization()(x)

    x = layers.Conv1DTranspose(32, kernelsize, strides=stride, activation='relu',
                              kernel_constraint=max_norm(max_norm_value), kernel_initializer='he_uniform')(x)

    #x = layers.BatchNormalization()(x)

    x = layers.Conv1DTranspose(1, kernelsize, strides=stride, activation='sigmoid',
                               kernel_constraint=max_norm(max_norm_value), kernel_initializer='he_uniform')(x)

    x = layers.Flatten()(x)

    autoencoder = keras.Model(autoencoderInput, x)

    autoencoder.compile(loss='binary_crossentropy', optimizer=keras.optimizers.Adam(1e-4),
                        metrics=['mean_absolute_error'],weighted_metrics=[])

    return autoencoder

def Classifier(resolution):
    descriminatorInput = keras.Input(shape=(resolution,))
    ticInput = keras.Input(shape=(1,))

    kernelsize = 3
    stride = 2
    max_norm_value = 2.0

    x = layers.Reshape((resolution, 1))(descriminatorInput)
    x = layers.Conv1D(2, kernelsize, strides=stride, activation='relu', kernel_constraint=max_norm(max_norm_value),
                      kernel_initializer='he_uniform')(x)

    x = layers.Conv1D(4, kernelsize, strides=stride, activation='relu', kernel_constraint=max_norm(max_norm_value),
                      kernel_initializer='he_uniform')(x)

    x = layers.Flatten()(x)

    x = layers.Dense(20, activation="relu")(x)

    x = keras.Model(descriminatorInput, x)

    tic = keras.Model(ticInput, layers.Dense(1, activation="linear")(ticInput))

    x = layers.concatenate([x.output, tic.output], axis=1)
    x = layers.Dense(10, activation="relu")(x)
    output = layers.Dense(2, activation="softmax")(x)

    classifier = keras.Model([descriminatorInput, ticInput], output, name="discriminator")

    classifier.compile(loss='binary_crossentropy', optimizer=keras.optimizers.Adam(1e-4),
                          metrics=['mean_absolute_error'])

    return classifier

def ClassifierLatent(resolution):
    descriminatorInput = keras.Input(shape=(resolution,))
    ticInput = keras.Input(shape=(1,))

    #x = layers.Dense(resolution, activation="relu")(descriminatorInput)

    x = layers.Layer()(descriminatorInput)

    x = keras.Model(descriminatorInput, x)

    tic = keras.Model(ticInput, layers.Dense(1, activation="linear")(ticInput))

    x = layers.concatenate([x.output, tic.output], axis=1)

    #x = layers.Dense(int(resolution), activation="relu")(x)

    #x = layers.Dense(int(resolution * 2), activation="relu")(x)

    #x = layers.Dense(resolution, activation="relu")(x)

    x = layers.Dense(5, activation="relu")(x)

    #x = layers.Dense(3, activation="relu")(x)

    output = layers.Dense(2, activation="softmax")(x)

    classifier = keras.Model([descriminatorInput, ticInput], output, name="discriminator")

    classifier.compile(loss='binary_crossentropy', optimizer=keras.optimizers.Adam(1e-4),
                          metrics=['mean_absolute_error'])

    return classifier


def makePRCPlot(pred,true,noSkill=True):

    prec, recall, threshs = met.precision_recall_curve(true, pred)

    auc = np.round(met.auc(recall, prec), 4)

    plt.plot(recall, prec, label="prAUC=" + str(auc))
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    if noSkill:
        numPositive = len([x for x in true if x > 0.5])
        numNegative = len(true) - numPositive
        plt.plot([0, 1.0],
                 [numPositive / float(numPositive + numNegative), numPositive / float(numPositive + numNegative)],
                 label="NSL prAUC=" + str(
                     np.round(numPositive / float(numPositive + numNegative), 4)))
    plt.legend()
    return auc


def findPeakBoundaries(peak):
    apex = int(len(peak)/2)
    #find left bound

    foundNewApex = True

    while(foundNewApex):
        foundNewApex = False

        x = apex
        while peak[x] > peak[apex] / 2 and x > 0:
            if peak[x] > peak[apex]:
                apex = x
            x -= 1
        lb = x

        x = apex
        while peak[x] > peak[apex] / 2 and x < len(peak) - 1:
            if peak[x] > peak[apex]:
                apex = x
                foundNewApex = True
            x += 1
        rb = x

    return lb,rb

def integratePeak(peak):
    lb,rb = findPeakBoundaries(peak)
    if lb != rb:
        area = np.trapz(peak[lb:rb],np.linspace(lb,rb,rb-lb))
    else:
        area = 0
    return area

