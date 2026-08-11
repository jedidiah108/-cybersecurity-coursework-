//java
//just implemented few things for task 7 
import java.nio.file.Files;
import java.nio.file.Path;

public class Task7_SynchronousCipher {

    // Generate Fibonacci-style keystream (byte version)
    static byte[] generateKeystream(int key, int length) {
        byte[] ks = new byte[length];
        ks[0] = (byte) (key & 0xFF);
        ks[1] = (byte) ((key + 1) & 0xFF);

        for (int i = 2; i < length; i++) {
            ks[i] = (byte) ((ks[i - 1] + ks[i - 2]) & 0xFF);
        }
        return ks;
    }

    // Encrypt / Decrypt (same operation)
    static void synchronousCipher(byte[] data, int key) {
        byte[] ks = generateKeystream(key, data.length);
        for (int i = 0; i < data.length; i++) {
            data[i] ^= ks[i];
        }
    }

    public static void main(String[] args) throws Exception {

        byte[] fileData = Files.readAllBytes(Path.of("bigfile.bin"));
        int key = 3;

        // Encryption
        long startEnc = System.nanoTime();
        synchronousCipher(fileData, key);
        long endEnc = System.nanoTime();

        // Decryption
        long startDec = System.nanoTime();
        synchronousCipher(fileData, key);
        long endDec = System.nanoTime();

        System.out.println("Synchronous cipher encryption time: "
                + (endEnc - startEnc) / 1_000_000.0 + " ms");
        System.out.println("Synchronous cipher decryption time: "
                + (endDec - startDec) / 1_000_000.0 + " ms");
    }
}
