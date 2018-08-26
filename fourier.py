import matplotlib.pyplot as plt
import math
import argparse
import sys


#samples per second (for plain frequency recordings)
SAMPLE_RATE_S = 100

#samples per cycle frequency (for winding rate)
SAMPLE_RATE_F = 100

#Time period for creating waves
MAX_TIME = 5

#max cycle frequency (MAX FREQUENCY THAT THE FOURIER CAN DETECT)
MAX_C_FREQ = 20


def createPlainWave(freq):
    record = []
    
    for i in range(int(SAMPLE_RATE_S * MAX_TIME)):
        record.append(math.sin(2 * math.pi * freq * i / SAMPLE_RATE_S))
    
    return record
    
def addWaves(wave1, wave2):
    result = []
    
    for i in range(len(wave1)):
        result.append(wave1[i] + wave2[i])
        
    return result
    
def fourier(compWave):
    result = []
    for cFreq in range(int(SAMPLE_RATE_F * MAX_C_FREQ)):
        totalX = 0
        totalY = 0
        for i in range(len(compWave)):
            totalX += compWave[i] * math.cos((i / SAMPLE_RATE_S) * (cFreq / SAMPLE_RATE_F) * 2 * math.pi)
            totalY += compWave[i] * math.sin((i / SAMPLE_RATE_S) * (cFreq / SAMPLE_RATE_F) * 2 * math.pi)
        result.append((totalX / len(compWave))**2 + (totalY / len(compWave))**2)
    return result
    
def display(wave, sampleRate):
    time = []
    for i in range(len(wave)):
        time.append(i / sampleRate)
        
    plt.plot(time, wave)
    plt.show()

def findPeaks(transformed):
    peaks = []
    i = 0
    status = 0 #0=below average, 1=above average, before peak, 2=above average, after peak
    av = 2 * sum(transformed) / len(transformed)
    while i < len(transformed):
        if (status == 1 and transformed[i-1] > transformed[i]):
            status = 2
            peaks.append((i-1) / SAMPLE_RATE_F)
        
        if (status == 0 and transformed[i] > av):
            status = 1
        if (status != 0 and transformed[i] < av):
            status = 0
            
        i += 1
    
    if status == 1:
        peaks.append((i-1) / SAMPLE_RATE_F)
    
    return peaks

if __name__=="__main__":
    const_help_msg = "SAMPLE_RATE_S: How many times the input plain sine waves are sampled per second. Default = 100.      " \
                + "MAX_TIME: Plain sine waves are sampled and recorded up to this time. Default = 5.      " \
                + "SAMPLE_RATE_F: The number of sampled possible component frequency per Hertz. Default = 100.      " \
                + "MAX_C_FREQ: The highest frequency the fourier transform tests (and can thus detect). Default = 20\n"
    
    parser = argparse.ArgumentParser(description="Perform a fourier transform on a test composite of given frequencies.")
    parser.add_argument('-c', '--const', type=float, nargs=4, help=const_help_msg, metavar=('SAMPLE_RATE_S', 'MAX_TIME', 'SAMPLE_RATE_F', 'MAX_C_FREQ'))
    parser.add_argument('-d', '--display', action='store_true')
    parser.add_argument('FREQ', nargs="+")
    
    args = parser.parse_args(sys.argv[1:])  
    
    if len(args.FREQ) == 0:
        print("NEEDS ARGUMENTS FOR INPUT WAVE FREQUENCIES")
    else:
        if (args.const != None):
            SAMPLE_RATE_S = args.const[0]
            MAX_TIME = args.const[1]
            SAMPLE_RATE_F = args.const[2]
            MAX_C_FREQ = args.const[3]
        comp_wave = createPlainWave(float(args.FREQ[0]))
        for f in args.FREQ[1:]:
            comp_wave = addWaves(comp_wave, createPlainWave(float(f)))
       
        
        result = fourier(comp_wave)
        print(findPeaks(result))
        print(sum(result)/len(result))
        if (args.display):
            display(comp_wave, SAMPLE_RATE_S)
            display(result, SAMPLE_RATE_F)