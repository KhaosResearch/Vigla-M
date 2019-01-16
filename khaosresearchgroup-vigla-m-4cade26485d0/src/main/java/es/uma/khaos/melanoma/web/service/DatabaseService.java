package es.uma.khaos.melanoma.web.service;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import es.uma.khaos.melanoma.web.beans.Patient;
import es.uma.khaos.melanoma.web.beans.Sample;
import es.uma.khaos.melanoma.web.beans.User;
import es.uma.khaos.melanoma.web.exception.DatabaseException;

public final class DatabaseService {
	
	private static DatabaseService instance;
	
	public DatabaseService() {}
	
	public static synchronized DatabaseService getInstance()  {
		if(instance == null) {
			instance = new DatabaseService();
		}
		return instance;
	}
	
	
	/*
	 * USER 
	 */
	
//	public User getUser(int id) throws Exception {
//		
//		User user = null;
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		ResultSet rs = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			stmt = conn.prepareStatement("select * from rules_users where id=?");
//			stmt.setInt(1, id);
//			
//			rs = stmt.executeQuery();
//			if (rs.next()) {
//				String name = rs.getString("name");
//				String surname = rs.getString("surname");
//				String email = rs.getString("email");
//				user = new User(id, name, surname, email);
//			}
//		
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (rs!=null) rs.close();
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//		
//		return user;
//	}
//	
//	public User getUser(String email) throws Exception {
//		
//		User user = null;
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		ResultSet rs = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			stmt = conn.prepareStatement("select * from rules_users where email=?");
//			stmt.setString(1, email);
//			
//			rs = stmt.executeQuery();
//			if (rs.next()) {
//				int id = rs.getInt("id");
//				String name = rs.getString("name");
//				String surname = rs.getString("surname");
//				boolean validated = rs.getBoolean("validated");
//				boolean admin = rs.getBoolean("admin");
//				user = new User(id, name, surname, email, validated, admin);
//			}
//		
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (rs!=null) rs.close();
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//		
//		return user;
//		
//	}
	
	public User getUser(String username, String password) throws Exception {
		
		User user = null;
		
		Connection conn = null;
		PreparedStatement stmt = null;
		ResultSet rs = null;
		
		try {
			
			Properties props = new Properties();
			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("melanoma.properties"));
			String dbUrl = props.getProperty("db.url");
			String dbUser = props.getProperty("db.user");
			String dbPassword = props.getProperty("db.password");
			
			Class.forName("oracle.jdbc.driver.OracleDriver");
			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
			
			stmt = conn.prepareStatement("select * from melanoma.usuarios where nombre_pantalla=? and password=?");
			stmt.setString(1, username);
			stmt.setString(2, password);
			
			rs = stmt.executeQuery();
			if (rs.next()) {
				int id = rs.getInt("id_usuario");
				String name = rs.getString("nombre");
				String surname = rs.getString("apellidos");
				String email = rs.getString("email");
				user = new User(id, username, name, surname, email);
			}
		
		} catch (SQLException e) {
			throw new DatabaseException(e);
		} catch (Exception e) {
			throw e;
		} finally {
			if (rs!=null) rs.close();
			if (stmt!=null) stmt.close();
			if (conn!=null) conn.close();
		}
		
		return user;
	}
		
//	public int getUserId(String email) throws Exception {
//		
//		int id = -1;
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		ResultSet rs = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			stmt = conn.prepareStatement("select id from rules_users where email=?");
//			stmt.setString(1, email);
//			
//			rs = stmt.executeQuery();
//			
//			while (rs.next()) {
//				id = rs.getInt("id");
//			}
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (rs!=null) rs.close();
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//		
//		return id;
//		
//	}
	
	/*
	 * PATIENT
	 */
	
	public List<String> getPatientsFromUser(int userId) throws Exception {
		
		List<String> results = new ArrayList<String>();
		
		Connection conn = null;
		PreparedStatement stmt = null;
		ResultSet rs = null;
		
		try {
			
			Properties props = new Properties();
			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("melanoma.properties"));
			String dbUrl = props.getProperty("db.url");
			String dbUser = props.getProperty("db.user");
			String dbPassword = props.getProperty("db.password");
			
			Class.forName("oracle.jdbc.driver.OracleDriver");
			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
			
			stmt = conn.prepareStatement("select codigo_paciente from melanoma.pacientes where id_usuario=?");
			stmt.setInt(1, userId);
			rs = stmt.executeQuery();
			
			while (rs.next()) {
				String patientId = rs.getString("codigo_paciente");
				results.add(patientId);
			}
		} catch (SQLException e) {
			throw new DatabaseException();
		} catch (Exception e) {
			throw e;
		} finally {
			if (rs!=null) rs.close();
			if (stmt!=null) stmt.close();
			if (conn!=null) conn.close();
		}
		
		return results;
		
	}
	
	public List<Patient> getPatientsAndSamplesFromMedic(int userId) throws Exception {
		
		List<Patient> patients = new ArrayList<>();
		
		Connection conn = null;
		PreparedStatement stmt = null;
		ResultSet rs = null;
		
		String query = "select p.codigo_paciente, p.sexo, p.fechanacimiento, p.antecedentes, " +
				"m.id_muestra, m.fecha_muestra, m.fecha_experimento " + 
				"from melanoma.pacientes p, melanoma.muestras m " + 
				"where p.id_usuario=? and p.codigo_paciente=m.codigo_paciente " + 
				"order by codigo_paciente, id_muestra";
		
		System.out.println(query);
		
		try {
			
			Properties props = new Properties();
			props.load(Thread.currentThread()
					.getContextClassLoader().getResourceAsStream("melanoma.properties"));
			String dbUrl = props.getProperty("db.url");
			String dbUser = props.getProperty("db.user");
			String dbPassword = props.getProperty("db.password");
			
			Class.forName("oracle.jdbc.driver.OracleDriver");
			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
			
			stmt = conn.prepareStatement(query);
			stmt.setInt(1, userId);
			rs = stmt.executeQuery();
			
			Patient patient = null;
			
			while (rs.next()) {
				int patientCode = rs.getInt("codigo_paciente");
				if (patient == null || patient.getCode() != patientCode) {
					if (patient != null) patients.add(patient);
					String sex = rs.getString("sexo");
					Timestamp bornDate = rs.getTimestamp("fechanacimiento");
					String background = rs.getString("antecedentes");
					patient = new Patient(patientCode, sex, bornDate, background);
				}
				int sampleId = rs.getInt("id_muestra");
				Timestamp sampleDate = rs.getTimestamp("fecha_muestra");
				Timestamp experimentDate = rs.getTimestamp("fecha_experimento");
				patient.getSamples().add(new Sample(sampleId, sampleDate, experimentDate));
			}
			if (patient != null) patients.add(patient);
				
		} catch (SQLException e) {
			e.printStackTrace();
			throw new DatabaseException();
		} catch (Exception e) {
			e.printStackTrace();
			throw e;
		} finally {
			if (rs!=null) rs.close();
			if (stmt!=null) stmt.close();
			if (conn!=null) conn.close();
		}
		
		return patients;
		
	}
	
	/*
	 * TOKEN
	 */
	
//	public List<Token> getTokens(String email) throws Exception {
//		int userId = getUserId(email);
//		return getTokens(userId);
//	}
//	
//	public List<Token> getTokens(int userId) throws Exception {
//		List<Token> tokens = new ArrayList<Token>();
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		ResultSet rs = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			stmt = conn.prepareStatement("select * from tokens where user_id=?");
//			stmt.setInt(1, userId);
//			
//			rs = stmt.executeQuery();
//			while (rs.next()) {
//				int id = rs.getInt("id");
//				String token = rs.getString("token");
//				tokens.add(new Token(id, token, userId));
//			}
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException("No se pudo conectar a la base de datos.");	
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (rs!=null) rs.close();
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//		
//		return tokens;
//	}
//	
//	public Token getToken(String email, int tokenId) throws Exception {
//		
//		Token result = null;
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		ResultSet rs = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			String query = "select b.* from users.rules_users a, users.tokens b "
//					+ "where a.email=? and b.id=? and a.id=b.user_id";
//			stmt = conn.prepareStatement(query);
//			stmt.setString(1, email);
//			stmt.setInt(2, tokenId);
//			rs = stmt.executeQuery();
//			
//			if (rs.next()) {
//				int id = rs.getInt("id");
//				String token = rs.getString("token");
//				int userId = rs.getInt("user_id");
//				result = new Token(id, token, userId);
//			}
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (rs!=null) rs.close();
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//		
//		return result;
//	}
//	
//	public Token getToken(String email, String token) throws Exception {
//		
//		Token result = null;
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		ResultSet rs = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			String query = "select b.* from users.rules_users a, users.tokens b "
//					+ "where a.email=? and b.token=? and a.id=b.user_id";
//			stmt = conn.prepareStatement(query);
//			stmt.setString(1, email);
//			stmt.setString(2, token);
//			rs = stmt.executeQuery();
//			
//			if (rs.next()) {
//				int id = rs.getInt("id");
//				int userId = rs.getInt("user_id");
//				result = new Token(id, token, userId);
//			}
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (rs!=null) rs.close();
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//		
//		return result;
//	}
//	
//	public void insertToken(String token, int userId) throws Exception {
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		
//		try {
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			stmt = conn.prepareStatement("insert into tokens (token, user_id) values (?,?)");
//			stmt.setString(1, token);
//			stmt.setInt(2, userId);
//			stmt.execute();
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//	}
//	
//	public void deleteToken(int tokenId) throws Exception {
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			String query = "delete from tokens where id=?";
//			stmt = conn.prepareStatement(query);
//			stmt.setInt(1, tokenId);
//			stmt.execute();
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//	}
//	
//	
//	/*
//	 * EXECUTION RESULT
//	 */
//	
//	public List<ExecutionResult> getExecutions(String email) throws Exception {
//		int userId = getUserId(email);
//		return getExecutions(userId);
//	}
//	
//	public List<ExecutionResult> getExecutions(int userId) throws Exception {
//		
//		List<ExecutionResult> results = new ArrayList<ExecutionResult>();
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		ResultSet rs = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			stmt = conn.prepareStatement("select * from rules_executions where user_id=? order by start_time desc");
//			stmt.setInt(1, userId);
//			
//			rs = stmt.executeQuery();
//			
//			while (rs.next()) {
//				int id = rs.getInt("id");
//				Timestamp startTime = rs.getTimestamp("start_time");
//				Timestamp endTime = rs.getTimestamp("end_time");
//				String state = rs.getString("state");
//				String token = rs.getString("token");
//				results.add(new ExecutionResult(id, startTime, endTime, state, token));
//			}
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (rs!=null) rs.close();
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//		
//		return results;
//		
//	}
//	
//	public List<String> getTokenExecutions(String email) throws Exception {
//		int userId = getUserId(email);
//		return getTokenExecutions(userId);
//	}
//	
//	public List<String> getTokenExecutions(int userId) throws Exception {
//		
//		List<String> results = new ArrayList<String>();
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		ResultSet rs = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			stmt = conn.prepareStatement("select distinct(token) from rules_executions where user_id=?");
//			stmt.setInt(1, userId);
//			rs = stmt.executeQuery();
//			
//			while (rs.next()) {
//				String token = rs.getString("token");
//				results.add(token);
//			}
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (rs!=null) rs.close();
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//		
//		return results;
//		
//	}
//	
//	public List<ExecutionResultAndUser> getExecutionsFromToken(String token) throws Exception {
//		
//		List<ExecutionResultAndUser> results = new ArrayList<ExecutionResultAndUser>();
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		ResultSet rs = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			stmt = conn.prepareStatement("select * from rules_executions a, rules_users b "
//					+ "where a.token=? and a.user_id=b.id order by start_time desc");
//			stmt.setString(1, token);
//			
//			rs = stmt.executeQuery();
//			
//			while (rs.next()) {
//				int id = rs.getInt("id");
//				Timestamp startTime = rs.getTimestamp("start_time");
//				Timestamp endTime = rs.getTimestamp("end_time");
//				String state = rs.getString("state");
//				String email = rs.getString("email");
//				results.add(new ExecutionResultAndUser(id, startTime, endTime, state, token, email));
//			}
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (rs!=null) rs.close();
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//		
//		return results;
//		
//	}
//	
//	public ExecutionResult getExecution(int executionId) throws Exception {
//		
//		ExecutionResult result = null;
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		ResultSet rs = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			String query = "select * from users.rules_executions "
//					+ "where id=?";
//			stmt = conn.prepareStatement(query);
//			stmt.setInt(1, executionId);
//			rs = stmt.executeQuery();
//			
//			if (rs.next()) {
//				int id = rs.getInt("id");
//				Timestamp startTime = rs.getTimestamp("start_time");
//				Timestamp endTime = rs.getTimestamp("end_time");
//				String state = rs.getString("state");
//				String token = rs.getString("token");
//				result = new ExecutionResult(id, startTime, endTime, state, token);
//			}
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (rs!=null) rs.close();
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//		
//		return result;
//		
//	}
//	
//	public ExecutionResult getExecution(String email, int executionId) throws Exception {
//		
//		ExecutionResult result = null;
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		ResultSet rs = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			String query = "select b.*, a.email from users.rules_users a, users.rules_executions b "
//					+ "where b.id=? and a.id=b.user_id";
//			stmt = conn.prepareStatement(query);
//			stmt.setInt(1, executionId);
//			rs = stmt.executeQuery();
//			
//			if (rs.next()) {
//				
//				int id = rs.getInt("id");
//				Timestamp startTime = rs.getTimestamp("start_time");
//				Timestamp endTime = rs.getTimestamp("end_time");
//				String state = rs.getString("state");
//				String token = rs.getString("token");
//				String ownerEmail = rs.getString("email");
//				
//				boolean allowed = false;
//				if (email.equals(ownerEmail)) allowed = true;
//				if (!allowed) {
//					List<Token> tokens = getTokens(email);
//					allowed = tokens.contains(new Token(token));
//				}
//				if (allowed) result = new ExecutionResult(id, startTime, endTime, state, token);
//			}
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (rs!=null) rs.close();
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//		
//		return result;
//		
//	}
//	
//	public boolean isRunning(String email) throws Exception {
//		
//		boolean res = false;
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		ResultSet rs = null;
//		
//		try {
//			
//			int userId = getUserId(email);
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			stmt = conn.prepareStatement("select * from rules_executions where user_id=? and state='Running'");
//			stmt.setInt(1, userId);
//			
//			rs = stmt.executeQuery();
//			
//			if (rs.next()) {
//				res = true;
//			}
//			
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (rs!=null) rs.close();
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//		
//		return res;
//		
//	}
//	
//	public int storeExecutionResult(String email, String token) throws Exception {
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		ResultSet rs = null;
//		int id = -1;
//		int userId = getUserId(email);
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			stmt = conn.prepareStatement("insert into rules_executions (user_id, token) values (?, ?)",
//					Statement.RETURN_GENERATED_KEYS);
//			stmt.setInt(1, userId);
//			stmt.setString(2, token);
//			stmt.executeUpdate();
//			rs = stmt.getGeneratedKeys();
//			if (rs.next()){
//			    id=rs.getInt(1);
//			}
//			
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (rs!=null) rs.close();
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//		
//		return id;
//	}
//	
//	public void setExecutionResultState(int executionId, String state) throws Exception {
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			stmt = conn.prepareStatement("update rules_executions set state=?, end_time=CURRENT_TIMESTAMP where id=?");
//			stmt.setString(1, state);
//			stmt.setInt(2, executionId);
//			stmt.executeUpdate();
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//	}
//	
//	public void deleteExecutionResult(int executionId) throws Exception {
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			String query = "delete from rules_executions where id=?";
//			stmt = conn.prepareStatement(query);
//			stmt.setInt(1, executionId);
//			stmt.execute();
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//	}
//	
//	
//	/*
//	 * RULES
//	 */
//	
//	private List<ExecutionResultRule> getExecutionResultRules(int executionId, String tableName, boolean twoRules) throws Exception {
//		
//		List<ExecutionResultRule> results = new ArrayList<ExecutionResultRule>();
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		ResultSet rs = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			stmt = conn.prepareStatement("select * from users."+tableName+" where execution_id=?");
//			stmt.setInt(1, executionId);
//			
//			rs = stmt.executeQuery();
//			
//			while (rs.next()) {
//				int profile = rs.getInt("profile");
//				String rule1, rule2 = null, url1, url2 = null;
//				if (twoRules) {
//					url1 = rs.getString("url1");
//					url2 = rs.getString("url2");
//					rule1 = rs.getString("rule1");
//					rule2 = rs.getString("rule2");
//				} else {
//					rule1 = rs.getString("rule");
//					url1 = rs.getString("url");
//				}
//				results.add(new ExecutionResultRule(profile, rule1, rule2, url1, url2));
//			}
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (rs!=null) rs.close();
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//		
//		return results;
//	}
//	
//	public List<ExecutionResultRule> getSameRules(int executionId) throws Exception {
//		return getExecutionResultRules(executionId, "same_rules", true);
//	}
//	
//	public List<ExecutionResultRule> getOverlappingRules(int executionId) throws Exception {
//		return getExecutionResultRules(executionId, "overlapping_rules", true);
//	}
//	
//	public List<ExecutionResultRule> getInconsistentRules(int executionId) throws Exception {
//		return getExecutionResultRules(executionId, "inconsistent_rules", false);
//	}
//
//	public List<ExecutionResultRule> getTautologicalRules(int executionId) throws Exception {
//		return getExecutionResultRules(executionId, "tautological_rules", false);
//	}
//	
//	public List<ExecutionResultRule> getContradictoryRules(int executionId) throws Exception {
//		return getExecutionResultRules(executionId, "contradictory_rules", true);
//	}
//	
//	private void storeResultRules(TupleQueryResult aResult, int executionId, String tableName, boolean twoRules) throws Exception {
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			while (aResult.hasNext()) {
//				
//				BindingSet bs = aResult.next();
//				String profileString = bs.getValue("profile").stringValue();
//				int profile = Integer.valueOf(profileString);
//				String rule1 = bs.getValue("rule1").stringValue();
//				String url1 = bs.getValue("url1").stringValue();
//				String rule2 = null, url2 = null;
//				if (twoRules) {
//					rule2 = bs.getValue("rule2").stringValue();
//					url2 = bs.getValue("url2").stringValue();
//				}
//				
//				String query =
//						"insert into "+tableName+
//						" (profile, rule, url, execution_id) values (?,?,?,?)";
//				if (twoRules) query = 
//						"insert into "+tableName+
//						" (profile, rule1, url1, execution_id, rule2, url2) values (?,?,?,?,?,?)";
//				
//				stmt = conn.prepareStatement(query);
//				
//				stmt.setInt(1, profile);
//				stmt.setString(2, rule1);
//				stmt.setString(3, url1);
//				stmt.setInt(4, executionId);
//				if (twoRules) {
//					stmt.setString(5, rule2);
//					stmt.setString(6, url2);
//				}
//				stmt.execute();
//			}
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//	}
//	
//	public void storeSameRules(TupleQueryResult aResult, int executionId) throws Exception {
//		storeResultRules(aResult, executionId, "same_rules", true);
//	}
//	
//	public void storeOverlappingRules(TupleQueryResult aResult, int executionId) throws Exception {
//		storeResultRules(aResult, executionId, "overlapping_rules", true);
//	}
//	
//	public void storeInconsistentRules(TupleQueryResult aResult, int executionId) throws Exception {
//		storeResultRules(aResult, executionId, "inconsistent_rules", false);
//	}
//	
//	public void storeTautologicalRules(TupleQueryResult aResult, int executionId) throws Exception {
//		storeResultRules(aResult, executionId, "tautological_rules", false);
//	}
//	
//	public void storeContradictoryRules(TupleQueryResult aResult, int executionId) throws Exception {
//		storeResultRules(aResult, executionId, "contradictory_rules", true);
//	}
//	
//	private void deleteResultRules(int executionId, String tableName) throws Exception {
//		
//		Connection conn = null;
//		PreparedStatement stmt = null;
//		
//		try {
//			
//			Properties props = new Properties();
//			props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("ecompass.properties"));
//			String dbUrl = props.getProperty("url");
//			String dbUser = props.getProperty("user");
//			String dbPassword = props.getProperty("password");
//			
//			Class.forName("com.mysql.jdbc.Driver");
//			conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
//			
//			String query = "delete from "+tableName+" where execution_id=?";
//			stmt = conn.prepareStatement(query);
//			stmt.setInt(1, executionId);
//			stmt.execute();
//		} catch (SQLException e) {
//			e.printStackTrace();
//			throw new DatabaseException();
//		} catch (Exception e) {
//			e.printStackTrace();
//			throw e;
//		} finally {
//			if (stmt!=null) stmt.close();
//			if (conn!=null) conn.close();
//		}
//	}
//	
//	public void deleteSameRules(int executionId) throws Exception {
//		deleteResultRules(executionId, "same_rules");
//	}
//	
//	public void deleteOverlappingRules(int executionId) throws Exception {
//		deleteResultRules(executionId, "overlapping_rules");
//	}
//	
//	public void deleteInconsistentRules(int executionId) throws Exception {
//		deleteResultRules(executionId, "inconsistent_rules");
//	}
//	
//	public void deleteTautologicalRules(int executionId) throws Exception {
//		deleteResultRules(executionId, "tautological_rules");
//	}
//	
//	public void deleteContradictoryRules(int executionId) throws Exception {
//		deleteResultRules(executionId, "contradictory_rules");
//	}
	
}
