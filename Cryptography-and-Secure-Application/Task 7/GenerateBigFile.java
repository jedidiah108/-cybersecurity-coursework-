import java.io.FileOutputStream;
import java.util.Random;

public class GenerateBigFile {
    public static void main(String[] args) throws Exception {
        int sizeMB = 200;
        byte[] buffer = new byte[1024 * 1024]; // 1 MB
        Random rand = new Random();

        try (FileOutputStream fos = new FileOutputStream("bigfile.bin")) {
            for (int i = 0; i < sizeMB; i++) {
                rand.nextBytes(buffer);
                fos.write(buffer);
            }
        }

        System.out.println("200 MB file bigfile.bin created.");
    }
}
