//package org.apache.commons.mail;


//package junitexamples.listener;
 
/**
 * Created by ONUR BASKIRT on 27.03.2016.
 */
 
import org.junit.Ignore;
import org.junit.runner.Description;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;
import org.junit.runner.notification.RunListener;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.BufferedWriter;
import java.io.FileWriter;
 
import java.util.Date;
 
public class MyExecutionListener extends RunListener {
 
    //Start and End time of the tests
    long startTime;
    long endTime;
    double teststartTime;
    double testendTime;
    static String Directory;
    long filetime;
    

    public static void method2(String fileName, String content) {   
        try {   
            FileWriter writer = new FileWriter(fileName, true);   
            writer.write(content);   
            writer.close();   
        } catch (IOException e) {   
            e.printStackTrace();   
        }   
    }   


    @Override
    public void testRunStarted(Description description) throws Exception {
        //Start time of the tests
        startTime = new Date().getTime();
        filetime = startTime;
        //Print the number of tests before the all tests execution.
        System.out.println("Tests started! Number of Test case: " + description.testCount() + "\n");
    }
 
    @Override
    public void testRunFinished(Result result) throws Exception {
        //End time of the tests
        endTime = new Date().getTime();
        //Print the below lines when all tests are finished.
        System.out.println("Tests finished! Number of test case: " + result.getRunCount());
        long elapsedSeconds = (endTime-startTime);
        System.out.println("Elapsed time of tests execution: " + elapsedSeconds +" seconds");
    }
 
    @Override
    public void testStarted(Description description) throws Exception {
        //Write the test name when it is started.
	teststartTime = new Date().getTime();
        System.out.println(description.getMethodName() + " test is starting...");
    }
 
    @Override
    public void testFinished(Description description) throws Exception {
        //Write the test name when it is finished.
	testendTime = new Date().getTime();
	System.out.println(testendTime);
	double testexecutionSecond = (testendTime - teststartTime);
	
	System.out.println(description.getMethodName() + " test is finished : execution with " + testexecutionSecond + " m seconds" );
	method2("time/" + Long.toString(filetime), description.getClassName() + '.'+ description.getMethodName() + "," + Double.toString(testexecutionSecond) + "\n");
    }
 
    @Override
    public void testFailure(Failure failure) throws Exception {
        //Write the test name when it is failed.
        System.out.println(failure.getDescription().getMethodName() + " test FAILED!!!");
    }
 
    //O.B: IntelliJ ignored by default. I did not succeed to run this method.
    //If you know any way to accomplish this, please write a comment.
    @Override
    public void testIgnored(Description description) throws Exception {
        super.testIgnored(description);
        Ignore ignore = description.getAnnotation(Ignore.class);
        String ignoreMessage = String.format(
                "@Ignore test method '%s()': '%s'",
                description.getMethodName(), ignore.value());
        System.out.println(ignoreMessage + "\n");
    }
}
