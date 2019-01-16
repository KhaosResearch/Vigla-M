<%@ page contentType="text/html; charset=iso-8859-1" language="java"
	import="es.uma.khaos.melanoma.web.service.DatabaseService, es.uma.khaos.melanoma.web.beans.User,
		es.uma.khaos.melanoma.web.exception.DatabaseException"
	errorPage="" %>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>Login</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>
<body>
<% 
String username = request.getParameter("username");
String pass = request.getParameter("pass");
String from = request.getParameter("from");

HttpSession sesion = request.getSession();

int redirect = 0;
//boolean admin = false;

try {
	
	User user = DatabaseService.getInstance().getUser(username, pass);
	if (user != null) {
		/*
		if (user.getValidated()) {
			redirect = 1;
			admin = user.getAdmin();
		}
		else redirect = 2;
		*/
		sesion.setAttribute("usuario", username);
		sesion.setAttribute("userId", user.getId());
		sesion.setAttribute("conectado","true");
		//if (admin) sesion.setAttribute("admin", "true");
		sesion.setAttribute("successMsg", "Login successful!");
		redirect = 1; // Common user
	}
	
} catch (DatabaseException e){
	sesion.setAttribute("errorMsg", "Error: Impossible to connect to the database. Contact with an administrator.");
	redirect = -1; // ErrorgetId
	e.printStackTrace();
} catch (Exception e) {
	redirect = -1; // Error
	e.printStackTrace();
}

if (redirect==0) {
	sesion.setAttribute("errorMsg", "Incorrect username and password!");
	if (from!=null) {
		response.sendRedirect("../login.jsp?from=" + from);
	} else {
		response.sendRedirect("../.");
	}
} else if (redirect==1) {
	if (from!=null) {
		response.sendRedirect("../" + from);
	} else {
		response.sendRedirect("../.");
	}
/*
} else if (redirect==2) {
	sesion.setAttribute("errorMsg", "You don't have access to the webapp. Wait until an administrator approves you.");
	response.sendRedirect("../.");
*/
} else {
	response.sendRedirect("../error.jsp");
}

%> 
</body>
</html>