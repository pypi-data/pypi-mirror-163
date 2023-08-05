r"""
Visualizer for the esc-stage of the sps algorithm
"""
from spinterface.sps_results.stage_visualizer.ivisstage import IVisStage
from pathlib import Path
from typing import Union, Tuple, List
from spinterface.inputs.lattice.CLattice import CLattice
from spinterface.visualizations.lattices.cvisualpyvista import CVisualPyVista
import pandas as pd


class CVisEsc(IVisStage):
    r"""

    """

    def __call__(self) -> None:
        r"""
        Excecutes the visualization for the displace stage
        """
        if self.strategy in [1]:
            self._visualize_escaped_configuration()
            self._visualize_eigenvector_start_end()

    def __init__(self, strategy: int, info_file: Union[Path, str],
                 camera_spin_files: Union[List[Tuple[float, float, float]], None] = None,
                 spinvisualization_technique: str = 'oop', arrowscale_evec: float = 30, resolution: Tuple[float,float]=(400,400))->None:
        r"""
        Initializes the visualizer for the escape-stage of SPS
        Args:
            strategy(int): escape strategy
            info_file(Path,str): the file which holds information about the locations
            of the corresponding files. It is always in the same directory as the sps.in therefore all paths in the info
            file are relative to this.
        """
        super().__init__(strategy, camera_spin_files)
        self.parent_directory = Path(info_file).parent
        self.arrowscale_evec = arrowscale_evec
        self.keys, self.esckeys, self.folders, self.spinfiles = self._read_info_file(info_file=info_file)
        self.spinvisualization_technique = spinvisualization_technique
        self.resolution = resolution

    @staticmethod
    def _read_info_file(info_file: Union[Path, str]) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
        r"""
        Reads the columns of the escape-info file.
        """
        df = pd.read_csv(info_file, sep=r'\s+')
        return df['DISPKEY'], df['ESCKEY'], df['folder'], df['spin_file']

    @property
    def stage(self) -> str:
        r"""
        Returns:
            the stage
        """
        return 'Escape'

    def _stagestrategytext(self) -> str:
        r"""
        Returns:
            the escape strategy in words
        """
        if self.strategy == 1:
            return 'Use modefollowing to escape the convex region.'
        else:
            return 'Describing text for this strategy not yet coded.'

    def _visualize_escaped_configuration(self):
        r"""
        Visualizes the spin configurations for all escaped configurations
        """
        for spinfile in self.spinfiles:
            print(f'Visualizig: {spinfile}...')
            l_latt = CLattice(source='STM', path=self.parent_directory / spinfile)
            if self.spinvisualization_technique == 'oop':
                l_visu = CVisualPyVista(lattice=l_latt, cam=self.spincam)
            elif self.spinvisualization_technique == 'ipoop':
                l_visu = CVisualPyVista(lattice=l_latt, cam=self.spincam, heatmap=True, heatmap_saturation=1.0)
            else:
                raise ValueError('Selected spin visualization technique is not coded yet!')
            pngfile = spinfile.replace('.dat', '.png')
            pngfile_splitted = pngfile.split('/')
            pngpath = self.parent_directory
            for pathpart in pngfile_splitted:
                pngpath = pngpath / pathpart
            l_visu(outpath=pngpath, resolution=self.resolution)
            l_visu.plotter.close()
            print('...done')

    def _visualize_eigenvector_start_end(self):
        r"""
        Visualizes the spin configurations for all displaced configurations
        """
        for spinfile in self.spinfiles:
            evecfile_end = spinfile.replace('spin', 'evec')
            if (self.parent_directory / evecfile_end).is_file():
                print(f'Visualizig: {evecfile_end}...')
                l_latt_end = CLattice(source='evec', path=self.parent_directory / evecfile_end)
                l_visu_end = CVisualPyVista(lattice=l_latt_end, cam=self.spincam, arrowscale=self.arrowscale_evec)
                pngfile_end = evecfile_end.replace('.dat', '.png')
                pngfile_splitted_end = pngfile_end.split('/')
                pngpath_end = self.parent_directory
                for pathpart in pngfile_splitted_end:
                    pngpath_end = pngpath_end / pathpart
                l_visu_end(outpath=pngpath_end, resolution=self.resolution)
                l_visu_end.plotter.close()
                print('...done')
            evecfile_start = evecfile_end.replace('end', '0')
            if (self.parent_directory / evecfile_start).is_file():
                print(f'Visualizig: {evecfile_start}...')
                l_latt_start = CLattice(source='evec', path=self.parent_directory / evecfile_start)
                l_visu_start = CVisualPyVista(lattice=l_latt_start, cam=self.spincam, arrowscale=self.arrowscale_evec)
                pngfile_start = evecfile_start.replace('.dat', '.png')
                pngfile_splitted_start = pngfile_start.split('/')
                pngpath_start = self.parent_directory
                for pathpart in pngfile_splitted_start:
                    pngpath_start = pngpath_start / pathpart
                l_visu_start(outpath=pngpath_start, resolution=self.resolution)
                l_visu_start.plotter.close()
                print('...done')
