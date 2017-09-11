package com.google.android.gms.samples.vision.face.facetracker;

// * Created by divya on 6/9/17.
//


import android.util.Log;

import org.json.*;
import com.loopj.android.http.*;

import java.io.File;
import java.io.FileNotFoundException;

import cz.msebera.android.httpclient.Header;

public class VGGAPI {
    public FaceTrackerActivity mActivity;

    public VGGAPI(FaceTrackerActivity a)
    {
        mActivity = a;
    }

    public void updateScore(double s){
        mActivity.score = 10 - (int)(s*10);
        mActivity.updateScore();
    }

    public boolean verifyUser(File img) throws JSONException, FileNotFoundException{
        // http://localhost:5000/biosecure/api/v1/verify

        RequestParams params = new RequestParams();
        params.put("image",img,"image/jpeg");
        VGGClient.post("verify", params, new JsonHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, JSONObject response) {
                // If the response is JSONObject instead of expected JSONArray
                //System.out.println("Output from Server .... \n");
                //System.out.println(response);
                Log.d("DEBUG" , "Successs : "+statusCode+response.toString());
                try {
                    double temp =  Double.parseDouble(response.get("score").toString());
                    updateScore(temp);
                }
                catch (JSONException e)
                {
                    Log.d("ERROR", e.toString());
                }
            }
            @Override

            public void onFailure(int statusCode, Header[] headers, String responseString, Throwable throwable) {

                if(responseString!=null)
                Log.d("DEBUG" , "onFailure : "+statusCode+" "+responseString);

            }

            @Override
            public void onFailure(int statusCode, Header[] headers, Throwable throwable, JSONObject response) {
                // If the response is JSONObject instead of expected JSONArray

                if(response!=null)
                Log.d("DEBUG" , "Failed : "+statusCode+response.toString());
            }      });

        return true;
    }


    public boolean enrollUser(File img) throws JSONException, FileNotFoundException {
        // http://localhost:5000/biosecure/api/v1/enroll

        RequestParams params = new RequestParams();
        params.put("image",img,"image/jpeg");

        VGGClient.post("enroll", params, new JsonHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, JSONObject response) {
                // If the response is JSONObject instead of expected JSONArray
                //System.out.println("Output from Server .... \n");
                //System.out.println(response);
                Log.d("DEBUG" , "Successs : "+statusCode);
            }
            @Override
            public void onFailure(int statusCode, Header[] headers, String responseString, Throwable throwable) {
                if(responseString!=null)
                Log.d("DEBUG" , "onFailure : "+statusCode+" "+responseString);
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, Throwable throwable, JSONObject response) {
                // If the response is JSONObject instead of expected JSONArray
                //System.out.println("Output from Server .... \n");
                //System.out.println(response);
                if(response!=null)
                    Log.d("DEBUG" , "Failed : "+statusCode+response.toString());
            }      });

        return true;
    }

}
