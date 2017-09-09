package com.google.android.gms.samples.vision.face.facetracker;

import static java.lang.Math.abs;

/**
 * Created by divya on 8/9/17.
 */

public class BBox {
    public int left;
    public int right;
    public int top;
    public int bottom;
    public int width;
    public int height;

    public void update(float l, float r, float t, float b){
        left = (int)l;
        right = (int)r;
        top = (int)t;
        bottom = (int)b;
        width = abs(right-left);
        height = abs(bottom-top);
    }
    public void update(int l, int r, int t, int b){
        left = l;
        right = r;
        top = t;
        bottom = b;
        width = abs(right-left);
        height = abs(bottom-top);
    }
}
