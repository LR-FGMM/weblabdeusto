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
* Author: FILLME
*
*/

package es.deusto.weblab.client.experiments.xilinx;

import com.google.gwt.core.client.GWT;
import com.google.gwt.core.client.RunAsyncCallback;

import es.deusto.weblab.client.configuration.IConfigurationRetriever;
import es.deusto.weblab.client.experiments.xilinx.ui.XilinxExperiment;
import es.deusto.weblab.client.lab.experiments.ExperimentCreator;
import es.deusto.weblab.client.lab.experiments.ExperimentFactory.IExperimentLoadedCallback;
import es.deusto.weblab.client.lab.experiments.ExperimentFactory.MobileSupport;
import es.deusto.weblab.client.lab.experiments.ExperimentParameter;
import es.deusto.weblab.client.lab.experiments.ExperimentParameterDefault;
import es.deusto.weblab.client.lab.experiments.IBoardBaseController;
import es.deusto.weblab.client.lab.experiments.IExperimentCreatorFactory;
import es.deusto.weblab.client.lab.experiments.IHasExperimentParameters;

public class XilinxCreatorFactory implements IExperimentCreatorFactory, IHasExperimentParameters {

	public static final ExperimentParameterDefault IS_MULTIRESOURCE_DEMO = new ExperimentParameterDefault("is.multiresource.demo", "Is a multiresource demo?", false);
	public static final ExperimentParameterDefault IS_DEMO = new ExperimentParameterDefault("is.demo", "Is a demo?", false);
	
	@Override
	public String getCodeName() {
		return "xilinx";
	}

	@Override
	public ExperimentCreator createExperimentCreator(final IConfigurationRetriever configurationRetriever) {
		return new ExperimentCreator(MobileSupport.limited, getCodeName()){
			@Override
			public void createWeb(final IBoardBaseController boardController, final IExperimentLoadedCallback callback) {
				GWT.runAsync(new RunAsyncCallback() {
					@Override
					public void onSuccess() {
						callback.onExperimentLoaded(new XilinxExperiment(
								configurationRetriever,
								boardController
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
		return new ExperimentParameter[] { IS_MULTIRESOURCE_DEMO, IS_DEMO };
	}

}
