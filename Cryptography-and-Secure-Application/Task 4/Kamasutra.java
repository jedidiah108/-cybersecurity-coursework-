import java.io.*;
import java.util.*;

public class Kamasutra {

    // Generate random keyfile (13 random pairs)
    private static void generateKey(String keyFile) throws IOException {
        List<Character> letters = new ArrayList<>();

        for (char c = 'a'; c <= 'z'; c++) {
            letters.add(c);
        }

        Collections.shuffle(letters);

        StringBuilder key = new StringBuilder();
        for (char c : letters) {
            key.append(c);
        }

        BufferedWriter writer = new BufferedWriter(new FileWriter(keyFile));
        writer.write(key.toString());
        writer.newLine();
        writer.close();
    }

    // Load keyfile and build pairing map
    private static Map<Character, Character> loadKey(String keyFile) throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(keyFile));
        String line = reader.readLine();
        reader.close();

        if (line == null || line.length() != 26) {
            throw new IOException("Invalid keyfile format");
        }

        Map<Character, Character> map = new HashMap<>();
        for (int i = 0; i < 26; i += 2) {
            char a = line.charAt(i);
            char b = line.charAt(i + 1);
            map.put(a, b);
            map.put(b, a);
        }
        return map;
    }

    // Encrypt / Decrypt (same operation)
    private static void processFile(
            String inputFile,
            String outputFile,
            Map<Character, Character> keyMap) throws IOException {

        BufferedReader reader = new BufferedReader(new FileReader(inputFile));
        BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile));

        int ch;
        while ((ch = reader.read()) != -1) {
            char c = (char) ch;

            if (c >= 'a' && c <= 'z') {
                c = keyMap.get(c);
            }

            writer.write(c);
        }

        reader.close();
        writer.close();
    }

    public static void main(String[] args) {
        try {
            if (args.length == 2 && args[0].equals("-k")) {
                generateKey(args[1]);
                System.out.println("Key generated in " + args[1]);
                return;
            }

            if (args.length != 4) {
                System.out.println("Usage:");
                System.out.println("kamasutra -k <keyfile.txt>");
                System.out.println("kamasutra -e <keyfile.txt> <plaintext.txt> <ciphertext.txt>");
                System.out.println("kamasutra -d <keyfile.txt> <ciphertext.txt> <plaintext.txt>");
                return;
            }

            String mode = args[0];
            String keyFile = args[1];
            String inputFile = args[2];
            String outputFile = args[3];

            Map<Character, Character> keyMap = loadKey(keyFile);

            if (mode.equals("-e") || mode.equals("-d")) {
                processFile(inputFile, outputFile, keyMap);
                System.out.println("Operation completed successfully.");
            } else {
                System.out.println("Invalid option");
            }

        } catch (IOException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
