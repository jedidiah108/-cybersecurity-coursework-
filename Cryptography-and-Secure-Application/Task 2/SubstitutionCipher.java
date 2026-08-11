import java.io.*;
import java.util.*;

public class SubstitutionCipher {

    // Build substitution key from keyword
    private static String buildKey(String keyword) {
        boolean[] used = new boolean[26];
        StringBuilder key = new StringBuilder();

        // Remove duplicate letters from keyword
        for (char c : keyword.toCharArray()) {
            if (Character.isLetter(c)) {
                c = Character.toUpperCase(c);
                if (!used[c - 'A']) {
                    used[c - 'A'] = true;
                    key.append(c);
                }
            }
        }

        // Append remaining letters in reverse order (Z to A)
        for (char c = 'Z'; c >= 'A'; c--) {
            if (!used[c - 'A']) {
                key.append(c);
            }
        }

        return key.toString();
    }

    // Encrypt or decrypt a file
    private static void processFile(
            String inputFile,
            String outputFile,
            String key,
            boolean encrypt) throws IOException {

        BufferedReader reader = new BufferedReader(new FileReader(inputFile));
        BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile));

        int ch;
        while ((ch = reader.read()) != -1) {
            char c = (char) ch;

            if (Character.isLetter(c)) {
                boolean lower = Character.isLowerCase(c);
                c = Character.toUpperCase(c);

                if (encrypt) {
                    c = key.charAt(c - 'A');
                } else {
                    c = (char) ('A' + key.indexOf(c));
                }

                if (lower) {
                    c = Character.toLowerCase(c);
                }
            }

            writer.write(c);
        }

        reader.close();
        writer.close();
    }

    public static void main(String[] args) {
        if (args.length != 4) {
            System.out.println("Usage:");
            System.out.println("java SubstitutionCipher <enc|dec> <keyword> <inputfile> <outputfile>");
            return;
        }

        String mode = args[0];
        String keyword = args[1];
        String inputFile = args[2];
        String outputFile = args[3];

        String key = buildKey(keyword);

        try {
            if (mode.equalsIgnoreCase("enc")) {
                processFile(inputFile, outputFile, key, true);
            } else if (mode.equalsIgnoreCase("dec")) {
                processFile(inputFile, outputFile, key, false);
            } else {
                System.out.println("Invalid mode. Use enc or dec.");
                return;
            }

            System.out.println("Operation completed successfully.");
        } catch (IOException e) {
            System.out.println("File error: " + e.getMessage());
        }
    }
}
