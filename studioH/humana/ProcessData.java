package com.humana;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class ProcessData {

	private static final Path OUT_FILE_PATH = Paths.get("c:/studioH/cleanData.tsv");
	private static final Path PARTIAL_OUT_FILE_PATH = Paths.get("c:/studioH/partialCleanData.tsv");
	private static final Path PARTIAL_OUT_FILE_PATH_UNIQUE = Paths.get(
			"c:/studioH/partialCleanData_" + LocalDateTime.now().atZone(ZoneId.systemDefault()).toEpochSecond() + ".tsv");

	private static final Path IN_FILE_PATH = Paths.get("c:/opt/data_again.tsv");
	private static final int TABPATTERN = 4;
	private static Path filePath;

	private boolean partialClean;
	private boolean uniquePartialFile;

	private List<byte[]> processData(int inDataPosition, int inDataLength) {

		ExecutorService executorService = new ThreadPoolExecutor(2, 2, 0L, TimeUnit.MILLISECONDS,
				new LinkedBlockingQueue<Runnable>());

		// submitting task collections
		List<Callable<byte[]>> callableList = new ArrayList<>();
		List<byte[]> listOfBytes = new ArrayList<>();

		int dataPosition = evalDataPosition(inDataPosition);
		int dataLength = evalDataLength(inDataLength);
		int dataSetSize = determineFileSize() / 2;

		// load the data from the file to a map for further processing.
		Map<Integer, byte[]> dataMap = loadData(dataSetSize);

		Callable<byte[]> firstDatasetCallable = () -> {
			return editData(dataMap.get(1), dataPosition, dataLength, dataSetSize);
		};

		Callable<byte[]> secondDatasetCallable = () -> {
			// account for a correction range that may span the two arrays of data.
			int adjustedLength = 0;
			int adjustedPosition = 0;
			if (dataPosition < dataSetSize) {
				if (dataPosition + dataLength > dataSetSize) {
					adjustedLength = dataLength - (dataSetSize - dataPosition);
				}
			} else {
				adjustedLength = dataLength;
				adjustedPosition = dataPosition / 2;
			}
			return editData(dataMap.get(2), adjustedPosition, adjustedLength, dataSetSize);
		};

		callableList.add(firstDatasetCallable);
		callableList.add(secondDatasetCallable);

		try {
			List<Future<byte[]>> futures = executorService.invokeAll(callableList);
			for (Future<byte[]> future : futures) {
				if (future.isDone()) {
					listOfBytes.add(future.get());
				}
			}
		} catch (InterruptedException | ExecutionException e) {
			System.err.println("an error occurred while invoking the array processing services.");
			e.printStackTrace();
		} finally {
			if (executorService != null) {
				executorService.shutdown();
			}
		}

		return listOfBytes;
	}

	private Map<Integer, byte[]> loadData(int datasetSize) {

		Map<Integer, byte[]> cArrayMap = new HashMap<>();
		int mapKey = 0;

		try (InputStream inputStream = Files.newInputStream(IN_FILE_PATH);
				BufferedInputStream bis = new BufferedInputStream(inputStream);) {
			while (bis.available() > 0) {
				byte[] cArray = new byte[datasetSize];
				Arrays.fill(cArray, (byte) 94);
				bis.read(cArray);
				cArrayMap.put(++mapKey, cArray);
			}
		} catch (IOException e1) {
			System.err.println("An error occurred while reading the data.tsv file.");
			e1.printStackTrace();
		}

		return cArrayMap;
	}

	private byte[] editData(byte[] inArray, int dataPosition, int dataLength, int dataSetSize) {

		int tabCounter = 0;
		int charCounter = 0;
		byte[] localCArray = new byte[inArray.length];
		System.arraycopy(inArray, 0, localCArray, 0, inArray.length);

		for (int x = 0; x < localCArray.length; x++) {
			// leave the iteration if there is no more valid data within the array.
			if (localCArray[x] == (byte) 94) {
				break;
			}

			if (localCArray[x] == '\t') {
				tabCounter++;
			}

			// bypass the EOL marker if it does not exist in the pattern that has
			// 4 tabs preceding it.
			if ((localCArray[x] == '\n')) {
				if (tabCounter == TABPATTERN) {
					tabCounter = 0;
				} else {
					if (!isPartialClean() || (isPartialClean()
							&& (charCounter >= dataPosition && charCounter <= dataPosition + dataLength))) {
						// account for the buffer space position if an LF value starts the array.
						if (charCounter > 3) {
							localCArray[x] = (byte) 32;
						}
					}
				}
			}
			charCounter++;
		}

		// int charMarker = defineCharMarker(cArray);
		int charMarker = defineCharMarker(localCArray);
		byte[] goodData = new byte[charMarker];
		System.arraycopy(localCArray, 0, goodData, 0, charMarker);

		return goodData;
	}

	private int defineCharMarker(byte[] cArray) {

		int marker = 0;
		for (int z = cArray.length - 1; z > 0; z--) {
			if (cArray[z] != (byte) 94) {
				marker = z;
				break;
			}
		}
		return marker + 1;
	}

	private void writeData(List<byte[]> processedData) {

		if (processedData == null) {
			System.err.println("---> Error: There is no data avilable to write to file.");
			return;
		}

		WriteData wd = WriteData.getInstance();
		wd.writeData(processedData, determineFilePath());
	}

	private int determineFileSize() {

		File f = new File(IN_FILE_PATH.toString());
		return (int) f.length();
	}

	private boolean determineIfPartial(int inDataPosition, int inDataLength) {

		int dataPosition = evalDataPosition(inDataPosition);
		int dataLength = evalDataLength(inDataLength);
		return dataPosition == 0 || dataLength == 0 ? false : true;
	}

	private Path determineFilePath() {

		if (isPartialClean()) {
			if (isUniquePartialFile()) {
				filePath = Paths.get(PARTIAL_OUT_FILE_PATH_UNIQUE.toString());
			} else {
				filePath = Paths.get(PARTIAL_OUT_FILE_PATH.toString());
			}
		} else {
			filePath = Paths.get(OUT_FILE_PATH.toString());
		}

		return filePath;
	}

	private int evalDataPosition(int inDataPosition) {
		return inDataPosition <= 0 ? 0 : inDataPosition;
	}

	private int evalDataLength(int inDataLength) {
		return inDataLength <= 0 ? 0 : inDataLength;
	}

	public static Path getFilePath() {
		return filePath;
	}

	private boolean isPartialClean() {
		return this.partialClean;
	}

	public boolean isUniquePartialFile() {
		return uniquePartialFile;
	}

	private void setPartialClean(boolean partialClean) {
		this.partialClean = partialClean;
	}

	public static void setFilePath(Path filePath) {
		ProcessData.filePath = filePath;
	}

	public void setUniquePartialFile(boolean uniquePartialFile) {
		this.uniquePartialFile = uniquePartialFile;
	}

	public static void main(String[] args) {

		int arg_dataPosition = 0;
		int arg_dataLength = 0;
		String arg_displayOutput = "N";
		String arg_uniquePartialFile = "N";

		if (args.length == 4) {
			try {
				arg_dataPosition = Integer.valueOf(args[0]);
				arg_dataLength = Integer.valueOf(args[1]);
				arg_displayOutput = args[2];
				arg_uniquePartialFile = args[3];
			} catch (NumberFormatException e) {
				System.err.println("Invalid values passed in via the argument list.");
				System.exit(1);
			}
		}

		ProcessData pd = new ProcessData();
		pd.setPartialClean(pd.determineIfPartial(arg_dataPosition, arg_dataLength));
		pd.setUniquePartialFile(arg_uniquePartialFile.equalsIgnoreCase("Y") ? true : false);
		pd.determineFilePath();

		List<byte[]> processedData = pd.processData(arg_dataPosition, arg_dataLength);
		pd.writeData(processedData);

		if (arg_displayOutput.equalsIgnoreCase("Y")) {
			DisplayData dd = DisplayData.getInstance();
			dd.displayCleanData(pd.determineFilePath());
		}

	}
}
