# SideProject_Fourier-Analysis
A very small proof of concept for simple fourier analysis. Based on this video (https://www.youtube.com/watch?v=spUNpyF58BY) by 3Blue1Brown.

This is an inefficient but intuitive method for calculating a fourier transform without numerically computing an integral (something which is admittedly much simpler mathematically). Instead, one can wind a function (f(t)) around the origin with some winding frequency (r = f(t), angle = wt). The fourier transform of that particular frequency (w) is given by the real part of the center of mass of the wound function.

There are little to no 
