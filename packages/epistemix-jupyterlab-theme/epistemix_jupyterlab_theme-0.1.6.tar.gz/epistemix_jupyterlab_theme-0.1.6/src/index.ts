import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ISplashScreen, IThemeManager } from '@jupyterlab/apputils';
import { ICodeMirror } from '@jupyterlab/codemirror';

import { registerFRED } from './fred-language';
import { registerStyles } from './styles';
import { registerSplash } from './splash';

const theme: JupyterFrontEndPlugin<void> = {
  id: 'epistemix_jupyterlab_theme:theme',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    registerStyles(manager);
  }
};

const fred: JupyterFrontEndPlugin<void> = {
  id: 'epistemix_jupyterlab_theme:fred',
  autoStart: true,
  requires: [ICodeMirror],
  activate: (app: JupyterFrontEnd, codeMirror: ICodeMirror) => {
    registerFRED(app, codeMirror.CodeMirror);
  }
};

const splash: JupyterFrontEndPlugin<ISplashScreen> = {
  id: 'epistemix_jupyterlab_theme:splash',
  autoStart: true,
  provides: ISplashScreen,
  activate: (app: JupyterFrontEnd) => {
    return registerSplash(app);
  }
};

const plugins = [theme, fred, splash];

export default plugins;
