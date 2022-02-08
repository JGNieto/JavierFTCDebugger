/*
You may need to add a package declaration here. Example:
package org.baylorschool.library.debugging;
*/

import java.io.PrintWriter;
import java.net.Socket;
import java.util.Locale;
import java.util.concurrent.Semaphore;

public class DebuggingClient {
    private static DebuggingClient instance = new DebuggingClient();
    public static DebuggingClient getInstance() {
        return instance;
    }

    private final static String laptopIpAddr = "192.168.43.97";
    private final static int port = 11468;

    private int x = 0;
    private int y = 0;
    private int heading = 0;

    private final Semaphore semaphore; // Coordinate threads.

    public DebuggingClient() {
        semaphore = new Semaphore(1);
    }

    private void run() {
        if (!semaphore.tryAcquire()) return;
        Socket socket = null;
        try {
            socket = new Socket(laptopIpAddr, port);
            PrintWriter printWriter = new PrintWriter(socket.getOutputStream(), true);

            // The version of the message is sent to allow for modifications in the future and possible
            // backwards compatibility. The version is a number followed by the letter v. Example: 1v
            // After the version, the format is x comma y comma heading semicolon. Example: 1v1353,512,74;
            // The values are sent as integers. The message is terminated by a semicolon.
            String output = String.format(Locale.US,"1v%d,%d,%d;", x, y, heading);
            printWriter.println(output);
            printWriter.close();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (socket != null)
                    socket.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        semaphore.release();
    }

    /**
     * Sends the data to the laptop.
     */
    public void update() {
        new Thread(this::run).start();
    }

    public void setX(int x) {
        this.x = x;
    }

    public void setY(int y) {
        this.y = y;
    }

    public void setHeading(int heading) {
        this.heading = heading;
    }
}