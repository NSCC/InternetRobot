package com.example.koss2.controller;

import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class MainActivity extends AppCompatActivity {
    InetAddress address;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        if (android.os.Build.VERSION.SDK_INT > 9)
        {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        Button forward;
        Button left;
        Button right;
        Button back;
        Button stop;
        Button IP;
        final TextView IPTxt;
        final EditText IPIn;

        IPTxt = findViewById(R.id.IPTxt);
        IPIn = findViewById(R.id.IPIn);
        IP = findViewById(R.id.IP);
        forward = findViewById(R.id.Forward);
        left = findViewById(R.id.Left);
        right = findViewById(R.id.Right);
        back = findViewById(R.id.Back);
        stop = findViewById(R.id.Stop);


        IP.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    address = InetAddress.getByName(IPIn.getText().toString());
                }catch (IOException e){
                    Toast.makeText(getApplicationContext(),"asd", Toast.LENGTH_LONG ).show();
                }
                IPTxt.setText(address.toString());
            }
        });

        forward.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (address != null) {
                    try {
                        DatagramSocket datagramSocket = new DatagramSocket();
                        byte[] buffer = "Forward".getBytes();

                        DatagramPacket packet = new DatagramPacket(
                                buffer, buffer.length, address, 8888);
                        datagramSocket.send(packet);
                    } catch (IOException e) {}
                }

                else {
                    Toast.makeText(getApplicationContext(), "IP Not set!", Toast.LENGTH_LONG).show();
                }
            }
        });


        back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (address != null) {
                    try {
                        DatagramSocket datagramSocket = new DatagramSocket();
                        byte[] buffer = "Back".getBytes();

                        DatagramPacket packet = new DatagramPacket(
                                buffer, buffer.length, address, 8888);
                        datagramSocket.send(packet);
                    } catch (IOException e) {}
                }
                else{
                    Toast.makeText(getApplicationContext(), "IP Not set!", Toast.LENGTH_LONG).show();
                }
            }
        });

        left.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (address != null) {
                    try {
                        DatagramSocket datagramSocket = new DatagramSocket();
                        byte[] buffer = "Left".getBytes();

                        DatagramPacket packet = new DatagramPacket(
                                buffer, buffer.length, address, 8888);
                        datagramSocket.send(packet);
                    } catch (IOException e) {}
                }
                else{
                    Toast.makeText(getApplicationContext(), "IP Not set!", Toast.LENGTH_LONG).show();
                }
            }
        });
        right.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (address != null) {

                    try {
                        DatagramSocket datagramSocket = new DatagramSocket();
                        byte[] buffer = "Right".getBytes();

                        DatagramPacket packet = new DatagramPacket(
                                buffer, buffer.length, address, 8888);
                        datagramSocket.send(packet);
                    } catch (IOException e) {}
                }
                else{
                    Toast.makeText(getApplicationContext(), "IP Not set!", Toast.LENGTH_LONG).show();
                }
            }

        });
        stop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (address != null) {

                    try {


                        DatagramSocket datagramSocket = new DatagramSocket();
                        byte[] buffer = "Stop".getBytes();

                        DatagramPacket packet = new DatagramPacket(
                                buffer, buffer.length, address, 8888);
                        datagramSocket.send(packet);
                    } catch (IOException e){}
                }
                else{
                    Toast.makeText(getApplicationContext(), "IP Not set!", Toast.LENGTH_LONG).show();
                }
            }
        });
    }
}
