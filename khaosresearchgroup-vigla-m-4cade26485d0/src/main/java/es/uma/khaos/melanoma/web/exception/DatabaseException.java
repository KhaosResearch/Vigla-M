package es.uma.khaos.melanoma.web.exception;

public class DatabaseException extends Exception {
	
	private static final long serialVersionUID = 1997753363232807009L;
	
	public DatabaseException() {	}
	
	public DatabaseException(String message) {
		super(message);
	}
	
	public DatabaseException(Throwable cause) {
		super(cause);
	}
	
	public DatabaseException(String message, Throwable cause) {
		super(message, cause);
	}
	
	public DatabaseException(String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}

}
