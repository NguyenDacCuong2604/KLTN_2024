package com.edu.nlu.document.util;

import java.io.File;
import java.io.InputStream;

public class FileUtil {
    private FileUtil() {
    }

    public static String getExtension(String filename) {
        return filename.substring(filename.lastIndexOf(".") + 1);
    }

}
