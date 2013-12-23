/*
* Copyright (C) 2005 onwards University of Deusto
* All rights reserved.
*
* This software is licensed as described in the file COPYING, which
* you should have received as part of this distribution.
*
* This software consists of contributions made by many individuals, 
* listed below:
*
* Author: Luis Rodriguez <luis.rodriguez@opendeusto.es>
*
*/

package es.deusto.weblab.client.lab.experiments.util.applets.js;


import com.google.gwt.core.client.GWT;
import com.google.gwt.core.client.RunAsyncCallback;

import es.deusto.weblab.client.configuration.IConfigurationRetriever;
import es.deusto.weblab.client.configuration.exceptions.ConfigurationException;
import es.deusto.weblab.client.lab.experiments.ExperimentCreator;
import es.deusto.weblab.client.lab.experiments.ExperimentFactory.IExperimentLoadedCallback;
import es.deusto.weblab.client.lab.experiments.ExperimentFactory.MobileSupport;
import es.deusto.weblab.client.lab.experiments.ExperimentParameter;
import es.deusto.weblab.client.lab.experiments.ExperimentParameterDefault;
import es.deusto.weblab.client.lab.experiments.IBoardBaseController;
import es.deusto.weblab.client.lab.experiments.IExperimentCreatorFactory;
import es.deusto.weblab.client.lab.experiments.IHasExperimentParameters;
import es.deusto.weblab.client.lab.experiments.exceptions.ExperimentCreatorInstanciationException;
import es.deusto.weblab.client.lab.experiments.util.applets.AbstractCreatorFactory;

public class JSAppCreatorFactory implements IExperimentCreatorFactory, IHasExperimentParameters {

	public static final ExperimentParameterDefault JS_FILE = new ExperimentParameterDefault("js.file", "JavaScript file", "");
	public static final ExperimentParameterDefault HTML_FILE = new ExperimentParameterDefault("html.file", "HTML file", "");
	public static final ExperimentParameterDefault PROVIDE_FILE_UPLOAD = new ExperimentParameterDefault("provide.file.upload", "Provide upload file", false);
	
	@Override
	public String getCodeName() {
		return "js";
	}

	@Override
	public ExperimentCreator createExperimentCreator(final IConfigurationRetriever configurationRetriever) throws ExperimentCreatorInstanciationException {
		
		final int width;
		final int height;
		final String jsfile;
		final String htmlfile;
		final boolean provideFileUpload;
		
		//final String message;
		
		try{
			width   = configurationRetriever.getIntProperty(AbstractCreatorFactory.WIDTH);
			height  = configurationRetriever.getIntProperty(AbstractCreatorFactory.HEIGHT);
			jsfile = configurationRetriever.getProperty(JS_FILE);
			htmlfile = configurationRetriever.getProperty(HTML_FILE);
			provideFileUpload = configurationRetriever.getBoolProperty(PROVIDE_FILE_UPLOAD);
			
			// Throw an exception if no file was specified. The configuration needs to specify either
			// an HTML or a JS script as base files.
			if(jsfile.length() == 0 && htmlfile.length() == 0)
				throw new ExperimentCreatorInstanciationException("Misconfigured experiment: " + getCodeName() + ": No base file was specified (either js.file or html.file need to be specified)");
		
			// Throw an exception if both a js file and an html were specified. The configuration may only
			// specify one of them.
			if(jsfile.length() > 0 && htmlfile.length() > 0)
				throw new ExperimentCreatorInstanciationException("Misconfigured experiment: " + getCodeName() + ": Both an HTML and a JS file were specified. Only one of the two properties may be set (either js.file or html.file)");
		
		}catch(ConfigurationException icve){
			throw new ExperimentCreatorInstanciationException("Misconfigured experiment: " + getCodeName() + ": " + icve.getMessage(), icve);
		}

		final String file = jsfile.length() > 0 ? jsfile : htmlfile;
		final boolean isJSFile = jsfile.length() > 0;
		
		return new ExperimentCreator(MobileSupport.disabled, getCodeName()){
			@Override
			public void createWeb(final IBoardBaseController boardController, final IExperimentLoadedCallback callback) {
				GWT.runAsync(new RunAsyncCallback() {
					@Override
					public void onSuccess() {
						callback.onExperimentLoaded(new JSExperiment(
								configurationRetriever,
								boardController,
								file,
								isJSFile,
								width, // TODO: Make these configurable. 
								height,
								provideFileUpload
							));
					}
					
					@Override
					public void onFailure(Throwable e){
						callback.onFailure(e);
					}
				});
			}
		};
	}
	
	@Override
	public ExperimentParameter[] getParameters() {
		return new ExperimentParameter [] { AbstractCreatorFactory.WIDTH, AbstractCreatorFactory.HEIGHT, AbstractCreatorFactory.MESSAGE, AbstractCreatorFactory.PAGE_FOOTER,
											JS_FILE, HTML_FILE, PROVIDE_FILE_UPLOAD };
	}

}
