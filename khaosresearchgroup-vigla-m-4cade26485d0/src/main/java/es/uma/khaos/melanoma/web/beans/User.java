package es.uma.khaos.melanoma.web.beans;

public class User {
	
	private int id;
	private String username;
	private String name;
	private String surname;
	private String email;
	
	public User(int id, String username, String name, String surname, String email) {
		super();
		this.id = id;
		this.username = username;
		this.name = name;
		this.surname = surname;
		this.email = email;
	}
	
	public int getId() {
		return id;
	}
	
	public String getUsername() {
		return username;
	}
	
	public String getName() {
		return name;
	}
	
	public String getSurname() {
		return surname;
	}
	
	public String getEmail() {
		return email;
	}
}
