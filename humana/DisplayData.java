package com.humana;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class DisplayData {

	private static DisplayData single_instance = null;
	private static final Charset OUT_CHARSET = StandardCharsets.UTF_8;

	private DisplayData() {

	}

	public static DisplayData getInstance() {
		if (single_instance == null)
			single_instance = new DisplayData();

		return single_instance;
	}

	protected void displayCleanData(Path filePath) {
		
		
		StringTokenizer st;
		try (BufferedReader br = Files.newBufferedReader(filePath, OUT_CHARSET)) {

			String dataRow = br.readLine();
			while (dataRow != null) {
				st = new StringTokenizer(dataRow, "\t");
				List<String> dataArray = new ArrayList<String>();
				while (st.hasMoreElements()) {
					dataArray.add(st.nextElement().toString());
				}
				for (String item : dataArray) {
					System.out.print(item + "  ");
				}
				System.out.println();
				dataRow = br.readLine();
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}