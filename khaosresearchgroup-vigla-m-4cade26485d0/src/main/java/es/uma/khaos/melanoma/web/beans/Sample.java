package es.uma.khaos.melanoma.web.beans;

import java.sql.Timestamp;

public class Sample {
	
	private int id;
	private Timestamp sampleDate;
	private Timestamp experimentDate;
	
	public Sample(int id, Timestamp sampleDate, Timestamp experimentDate) {
		super();
		this.id = id;
		this.sampleDate = sampleDate;
		this.experimentDate = experimentDate;
	}

	public int getId() {
		return id;
	}

	public Timestamp getSampleDate() {
		return sampleDate;
	}

	public Timestamp getExperimentDate() {
		return experimentDate;
	}
	
}
