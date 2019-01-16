package es.uma.khaos.melanoma.web.service;

import java.util.List;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import es.uma.khaos.melanoma.web.beans.Patient;

public class JSONService {
	
	private static JSONService instance;
	
	public JSONService() {}
	
	public static synchronized JSONService getInstance()  {
		if(instance == null) {
			instance = new JSONService();
		}
		return instance;
	}
	
	public String convert(Object obj) {
		String res = "";
		ObjectMapper mapper = new ObjectMapper();
		try {
			res = mapper.writeValueAsString(obj);
		} catch (JsonProcessingException e) {
			e.printStackTrace();
		}
		return res;
	}
	
	public static void main(String[] args) throws Exception {
		List<Patient> p = DatabaseService.getInstance().getPatientsAndSamplesFromMedic(1164);
		System.out.println(p);
		System.out.println(JSONService.getInstance().convert(p));
	}

}
