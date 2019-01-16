package es.uma.khaos.melanoma.web.api;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.util.*;


import javax.servlet.ServletContext;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.Response.ResponseBuilder;
import javax.ws.rs.core.Response.Status;

import es.uma.khaos.melanoma.web.beans.Patient;
import es.uma.khaos.melanoma.web.exception.PythonException;
import es.uma.khaos.melanoma.web.service.DatabaseService;

@Path("/")
public class MelanomaRESTService {
	
	private final boolean test = false;
	
	private final String clusterHeatmapCommand = "run-clustermaps.sh";
	private final String correlationCommand= "run-correlation.sh";
	private final String geneRegNetworkCommand = "run-GRN.sh";

	@Context
    private ServletContext context;
	
	@GET
	@Path("/db/patients_and_samples")
	@Produces(MediaType.APPLICATION_JSON)
	public Response getPatientsAndSamples(@Context HttpServletRequest request) throws Exception {
		HttpSession session = request.getSession();
		if (session == null || session.getAttribute("userId")==null) {
			return Response.status(Status.FORBIDDEN).build();
		} else {
			int userId = (Integer) session.getAttribute("userId");
			List<Patient> patients =
					DatabaseService.getInstance().getPatientsAndSamplesFromMedic(userId);
			// return HTTP response 200 in case of success
			return Response.status(200).entity(patients).build();
		}
	}
	
	@GET
	@Path("/img/{id}")
	@Produces("image/png")
	public Response getImg(
			@PathParam(value="id") String imageId,
			@Context HttpServletRequest request) throws Exception {
		HttpSession session = request.getSession();
		if (session == null || session.getAttribute("userId")==null) {
			return Response.status(Status.FORBIDDEN).build();
		} else {
			try {
				File tmpDir = (File)context.getAttribute("javax.servlet.context.tempdir");
				if(null == tmpDir)
					throw new IllegalStateException("Container does not provide a temp dir");
				System.out.println("TEMPDIR");
				System.out.println(tmpDir);

				File imageFile = new File(tmpDir, imageId);
				System.out.println("IMAGEID");
				System.out.println(imageId);

				FileInputStream fileInputStream = new FileInputStream(imageFile);
				ResponseBuilder responseBuilder = Response.ok((Object) fileInputStream);
				responseBuilder.type("image/png");
			    responseBuilder.header("Content-Disposition", "inline; filename="+imageId+".png");
				return responseBuilder.build();
				
			} catch (Exception e) {
				e.printStackTrace();
				return Response.serverError().build();
			}
		}
	}

	@GET
	@Path("/service/cluster_heatmap")
	@Produces({ MediaType.TEXT_PLAIN })
	public Response getHeatmap(
			@QueryParam(value = "id") List<Integer> ids,
			@QueryParam(value = "label") List<String> labels,
			@QueryParam(value = "percentage") double percentage,
			@Context HttpServletRequest request) throws Exception {

		System.out.println("Lista de ID");
		System.out.println(ids);
		System.out.println("Lista de Labels");
		System.out.println(labels);

		Properties props = new Properties();
		props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("melanoma.properties"));
		String scriptDirectory = props.getProperty("scripts.directory");

		String[] cmd = new String[] {
				scriptDirectory+clusterHeatmapCommand ,
				//clusterHeatmapCommand,
				ids.toString().replaceAll(" ", ""),
				formatStringListToPython(labels).replaceAll(" ", ""),
				String.format(Locale.US, "%.2f", percentage)
		};
		return getPythonGeneratedHTML(cmd, request);

	}

	@GET
	@Path("/service/gene_regulatory_network")
	@Produces({ MediaType.TEXT_PLAIN })
	public Response getGeneRegNetwork(
			@QueryParam(value = "id") List<Integer> ids,
			@QueryParam(value = "label") List<String> labels,
			@QueryParam(value = "percentage1") double percentage1,
			@QueryParam(value = "max_links") int maxLinks,
			@Context HttpServletRequest request) throws Exception {


		Properties props = new Properties();
		props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("melanoma.properties"));
		String scriptDirectory = props.getProperty("scripts.directory");



		String[] cmd = new String[] {
				scriptDirectory+geneRegNetworkCommand,
				//geneRegNetworkCommand,
				ids.toString().replaceAll(" ", ""),
				formatStringListToPython(labels).replaceAll(" ", ""),
				String.format(Locale.US, "%.2f", percentage1),
				String.valueOf(maxLinks)
			};

			return getPythonGeneratedHTML(cmd,request);
		}


	@GET
	@Path("/service/correlation")
	@Produces("image/png")
	public Response getCorrelation(
			@QueryParam(value = "id") List<Integer> ids,
			@QueryParam(value = "label") List<String> labels,
			@QueryParam(value = "percentage") double percentage,
			@Context HttpServletRequest request) throws Exception {

		/*
		Properties props = new Properties();
		props.load(Thread.currentThread().getContextClassLoader().getResourceAsStream("melanoma.properties"));
		String scriptDirectory = props.getProperty("scripts.directory");
		*/

		String[] cmd = new String[] {
				//scriptDirectory+correlationCommand ,
				correlationCommand ,
				ids.toString().replaceAll(" ", ""),
				formatStringListToPython(labels).replaceAll(" ", ""),
				String.format(Locale.US, "%.2f", percentage)
		};
		return getPythonGeneratedImage(cmd, request);

	}

	private Response getPythonGeneratedImage(String []  cmd, HttpServletRequest request) {
		HttpSession session = request.getSession();
		if (session == null || session.getAttribute("userId")==null) {
			return Response.status(Status.FORBIDDEN).build();
		}
		//TODO: Comprobar que samples pertenecen a userId
		//int userId = (Integer) session.getAttribute("userId");

		System.out.println(cmd);
			
		try {

		    String path = executeCommand(cmd);

            File imageFile = new File(path); //remove file:
				
			File imageId = createTempFile(imageFile, "png", session);
			imageFile.delete();

			return Response.ok(path).build();
		}
		catch (Exception e) {
		    e.printStackTrace();
		    return Response.serverError().build();

		}
	}

	private Response getPythonGeneratedHTML(String [] cmd, HttpServletRequest request) {
		HttpSession session = request.getSession();

		System.out.println("CMD");
		System.out.println(cmd);

		try {

			String htmlpath = executeCommand(cmd);
			System.out.println("HTMLPATH: " + htmlpath);

			//File imageFile = new File(htmlpath); //remove file:

//			File imageId = createTempFile(imageFile,"html", session);
//			System.out.println("imageId");
//			System.out.println(imageId);
			//imageFile.delete();

			return Response.ok(htmlpath).build();
		}
		catch (Exception e) {
			e.printStackTrace();
			return Response.serverError().build();

		}
	}


	@GET
	@Path("/service/missi")
	//@Produces("image/png")
	@Produces({ MediaType.TEXT_HTML, MediaType.APPLICATION_XML, MediaType.APPLICATION_JSON })
	public Response getMissi(@Context HttpServletRequest request) throws Exception {
		
		HttpSession session = request.getSession();
			
		try {
			
			String realPath = context.getRealPath("WEB-INF/img/bokeh_2018-09-26_090453.json");
			System.out.println("RealPath: " + realPath);
			File imageFile = new File(realPath);

			// uncomment line below to send non-streamed
			// return Response.ok(imageData).build();
			
			//sleep 5 seconds
			//Thread.sleep(5000);
			
			File imageId = createTempFile(imageFile, "html", session);
			return Response.ok(imageId).build();
			
		} catch (Exception e) {
			e.printStackTrace();
			return Response.serverError().build();
		}
	}
	
	private String executeCommand(String [] command) throws IOException, PythonException {
		int lines = 0;
		String line, ret = "";
		Process p = Runtime.getRuntime().exec(command);
		System.out.println("Process");
		System.out.println(p);

		BufferedReader stdInput = new BufferedReader(new InputStreamReader(
                p.getInputStream()));

        BufferedReader stdError = new BufferedReader(new InputStreamReader(
                p.getErrorStream()));
		
		ret = stdInput.readLine();
		while ((line = stdInput.readLine()) != null) {
			ret += "\n" + line;
			lines++;
		}
		System.out.println("COMMAND ERROR:");
		while ((line = stdError.readLine()) != null) {
			System.out.println(line);
		}
		stdError.close();
		stdInput.close();
	//	while(ret.startsWith("file://"))
	//	{
	//		ret = ret.replaceFirst("file://", "");

	//	}

		/*if (lines>0) {
			throw new PythonException(ret);
		}*/
		System.out.println("RETURN : " + ret);

		return ret;
	}
	
	private String formatStringListToPython(List<String> list) {
		return list.toString().replaceAll("\\[", "\\[\'").replaceAll("\\]", "\'\\]").replaceAll(", ", "\', \'");
	}
	
//	private String createTempFile(File source) throws IOException {
//		return createTempFile(source, null);
//	}
	
	@SuppressWarnings("unchecked")
	private File createTempFile(File source, String ext, HttpSession session) throws IOException {
		File tmpDir = (File)context.getAttribute("javax.servlet.context.tempdir");
		System.out.println(tmpDir);
		System.out.println("TMPDIR");

		if(null == tmpDir)
		  throw new IllegalStateException("Container does not provide a temp dir"); // Or handle otherwise
		
		String imageId = UUID.randomUUID().toString();
		if (ext != null) imageId += "."+ext;

		File targetFile = new File(tmpDir, imageId);
		Files.copy(source.toPath(), targetFile.toPath());
		System.out.println(targetFile.toPath());
		List<String> sessionImgs = (List<String>) session.getAttribute("imgs");
		sessionImgs.add(targetFile.getAbsolutePath());
		
		return targetFile;
	}
	
}
