package com.google.android.gms.samples.vision.face.facetracker;

import android.os.AsyncTask;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

/**
 * Created by divya on 6/9/17.
 */

import org.json.*;
import com.loopj.android.http.*;
import cz.msebera.android.httpclient.entity.StringEntity;
import android.content.Context;

public class VGGClient {
    // TODO: Add your own IP address
    //private static final String BASE_URL = "http://192.168.1.32:5000/biosecure/api/v1/";
    //private static final String BASE_URL = "http://192.168.1.25:5000/biosecure/api/v1/";
    private static final String BASE_URL = "http://face.comp.nus.edu.sg/CA/biosecure/api/v1/";

    private static AsyncHttpClient client = new AsyncHttpClient();



    public static void get(String url, RequestParams params, AsyncHttpResponseHandler responseHandler) {
        client.get(getAbsoluteUrl(url), params, responseHandler);
    }

    public static void post(String url,RequestParams  params, JsonHttpResponseHandler  responseHandler) {
        client.post(getAbsoluteUrl(url), params , responseHandler);
    }

    private static String getAbsoluteUrl(String relativeUrl) {
        return BASE_URL + relativeUrl;
    }
}

/*

public class VGGClient extends AsyncTask<String, Void, String> {

    public static final String REQUEST_METHOD = "POST";
    public static final int READ_TIMEOUT = 15000;
    public static final int CONNECTION_TIMEOUT = 15000;

    @Override
    protected String doInBackground(String... params){
        String stringUrl = params[0];
        String result;
        String inputLine;
        try {
                //Create a URL object holding our url
                URL myUrl = new URL(stringUrl);

                //Create a connection
                HttpURLConnection connection =(HttpURLConnection)
                        myUrl.openConnection();

                //Set methods and timeouts
                connection.setRequestMethod(REQUEST_METHOD);
                connection.setReadTimeout(READ_TIMEOUT);
                connection.setConnectTimeout(CONNECTION_TIMEOUT);
                connection.setDoInput(true);
                connection.setDoOutput(true);
                //Connect to our url
                connection.connect();

                connection.getOutputStream().write( ("data=" + "Test").getBytes());
                //Create a new InputStreamReader
                InputStreamReader streamReader = new
                        InputStreamReader(connection.getInputStream());

                //Create a new buffered reader and String Builder
                BufferedReader reader = new BufferedReader(streamReader);
                StringBuilder stringBuilder = new StringBuilder();

                //Check if the line we are reading is not null
                while((inputLine = reader.readLine()) != null){
                    stringBuilder.append(inputLine);
                }

                //Close our InputStream and Buffered reader
                reader.close();
                streamReader.close();
                connection.disconnect();
                //Set our result equal to our stringBuilder
                result = stringBuilder.toString();

        } catch (MalformedURLException e) {
            e.printStackTrace();
            result = null;
        } catch (IOException e) {
            e.printStackTrace();
            result = null;
        }
        return result;
    }

    @Override
    protected void onPostExecute(String result){
        super.onPostExecute(result);
    }
}*/
