package es.uma.khaos.melanoma.web.listener;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import javax.servlet.http.HttpSessionEvent;
import javax.servlet.http.HttpSessionListener;

public class MelanomaSessionListener implements HttpSessionListener {

    @Override
    public void sessionCreated(HttpSessionEvent e) {
        System.out.println("sessionCreated");
        e.getSession().setAttribute("imgs", new ArrayList<String>());
    }

    @Override
    @SuppressWarnings("unchecked")
    public void sessionDestroyed(HttpSessionEvent e) {
        System.out.println("sessionDestroyed");
        List<String> sessionImgs = (List<String>) e.getSession().getAttribute("imgs");
        for (String i : sessionImgs) {
        	File f = new File (i);
        	if(f.exists()) f.delete();
        }
    }
}