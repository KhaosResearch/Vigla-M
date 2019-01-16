package es.uma.khaos.melanoma.web.api;


import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.python.util.PythonInterpreter;
import org.python.core.*;


public class Comprobacion {


    public static void main(String[] args) {
        leerPython2();

    }

    public static void leerPython()
    {
        try
        {
            String argsToPythonInterpreter = "/home/khaosdev/AnacondaProjects/PGenes/run-clustermaps.py";
            Runtime app = Runtime.getRuntime();
            Process pr= app.exec("python " + argsToPythonInterpreter);

            System.out.println(pr);
        }
        catch (IOException ex)
        {


            System.out.println( ex.getMessage() );
        }
    }
    public static void leerPython2()
    {
        PythonInterpreter interpreter = new PythonInterpreter();
        interpreter.exec("import run-clustermaps");
        PyObject func = interpreter.get("run-clustermaps");
        System.out.println(func.__call__().__tojava__(String.class));
    }

}