package com.humana;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.file.Path;
import java.util.List;

public class WriteData {

	private static WriteData single_instance = null;
	
	private WriteData() {

	}

	public static WriteData getInstance() {
		if (single_instance == null)
			single_instance = new WriteData();

		return single_instance;
	}

	protected void writeData(List<byte[]> processedData, Path filePath) {

		if (processedData == null) {
			System.err.println("---> Error: no data to write to the " + filePath.getFileName() + " file.");
			return;
		}

		try (OutputStreamWriter writer = new OutputStreamWriter(new FileOutputStream(filePath.toString()))) {
			for (byte[] bList : processedData) {
				writer.write(new String(bList, "UTF-8"));
				writer.flush();
			}
		} catch (IOException e1) {
			System.err.println("An error occurred while writing to the cleanData.tsv file.");
			e1.printStackTrace();
		}
	}

}