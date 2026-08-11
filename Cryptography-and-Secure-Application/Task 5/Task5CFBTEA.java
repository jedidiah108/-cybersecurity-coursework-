import java.nio.charset.StandardCharsets;

public class Task5CFBTEA {

    /* ===== TEA ENCRYPTION ===== */
    public static void encrypt(int[] v, int[] k) {
        int v0 = v[0], v1 = v[1];
        int sum = 0;
        int delta = 0x9e3779b9;

        for (int i = 0; i < 32; i++) {
            sum += delta;
            v0 += ((v1 << 4) + k[0]) ^ (v1 + sum) ^ ((v1 >>> 5) + k[1]);
            v1 += ((v0 << 4) + k[2]) ^ (v0 + sum) ^ ((v0 >>> 5) + k[3]);
        }

        v[0] = v0;
        v[1] = v1;
    }

    /* ===== CFB ENCRYPTION (s-bit) ===== */
    public static void cfbEncrypt(byte[] plaintext, int s) {
        int[] SR = {0x00000000, 0x00000000}; // 64-bit shift register (IV)
        int[] key = {1, 2, 3, 4};            // Fixed 128-bit key

        int bitLength = plaintext.length * 8;
        int bitPos = 0;

        while (bitPos < bitLength) {
            int[] temp = {SR[0], SR[1]};
            encrypt(temp, key);

            // Extract s MSBs from TEA output
            int keystream = temp[0] >>> (32 - s);

            // Extract s plaintext bits
            int byteIndex = bitPos / 8;
            int bitOffset = bitPos % 8;
            int p = (plaintext[byteIndex] >>> (8 - s - bitOffset)) & ((1 << s) - 1);

            int c = p ^ keystream;

            // Shift register update
            SR[0] = (SR[0] << s) | c;
            bitPos += s;
        }
    }

    public static void main(String[] args) {

        /* ===== STUDENT NUMBER ===== */
        String studentID = "8876149";
        byte[] plaintext = studentID.getBytes(StandardCharsets.US_ASCII);

        /* ===== 2-bit CFB ===== */
        long start2 = System.nanoTime();
        cfbEncrypt(plaintext, 2);
        long end2 = System.nanoTime();

        /* ===== 3-bit CFB (c = 3) ===== */
        long start3 = System.nanoTime();
        cfbEncrypt(plaintext, 3);
        long end3 = System.nanoTime();

        double time2 = (end2 - start2) / 1_000_000.0;
        double time3 = (end3 - start3) / 1_000_000.0;

        System.out.println("2-bit CFB TEA time: " + time2 + " ms");
        System.out.println("3-bit CFB TEA time: " + time3 + " ms");
    }
}
