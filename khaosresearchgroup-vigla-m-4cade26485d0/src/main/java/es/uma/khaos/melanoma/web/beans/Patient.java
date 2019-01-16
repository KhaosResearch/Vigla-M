package es.uma.khaos.melanoma.web.beans;

import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement
public class Patient {
	
	private int code;
	private String sex;
	private Timestamp bornDate;
	private String record;
	
	private List<Sample> samples;
	
	public Patient(int code, String sex, Timestamp bornDate, String record) {
		super();
		this.code = code;
		this.sex = translateSex(sex);
		this.bornDate = bornDate;
		this.record = record;
		this.samples = new ArrayList<>();
	}

	public int getCode() {
		return code;
	}

	public String getSex() {
		return sex;
	}

	public Timestamp getBornDate() {
		return bornDate;
	}

	public String getRecord() {
		return record;
	}

	public List<Sample> getSamples() {
		return samples;
	}
	
	private String translateSex(String sex) {
		if ("Varon".equals(sex)) return "Male";
		if ("Mujer".equals(sex)) return "Female";
		return sex;
	}

}
