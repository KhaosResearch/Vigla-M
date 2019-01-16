package es.uma.khaos.melanoma.web.exception;

public class PythonException extends Exception {
	
	private static final long serialVersionUID = 1L;

	public PythonException() {	}
	
	public PythonException(String message) {
		super(message);
	}
	
	public PythonException(Throwable cause) {
		super(cause);
	}
	
	public PythonException(String message, Throwable cause) {
		super(message, cause);
	}
	
	public PythonException(String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}

}