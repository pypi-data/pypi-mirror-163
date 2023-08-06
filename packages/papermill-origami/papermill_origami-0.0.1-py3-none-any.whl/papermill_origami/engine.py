"""This module holds the NoteableEngine class used to register the noteable engine with papermill.

It enables papermill to run notebooks against Noteable as though it were executing a notebook locally.
"""

import logging
from contextlib import asynccontextmanager
from typing import Generator, Optional

from jupyter_client import KernelManager
from jupyter_client.utils import run_sync
from nbclient.exceptions import CellExecutionError
from nbformat import NotebookNode
from origami.client import NoteableClient
from origami.types.files import NotebookFile
from papermill.engines import Engine, NotebookExecutionManager

from .manager import NoteableKernelManager

logger = logging.getLogger(__name__)


class NoteableEngine(Engine):
    """The subclass that can be registered with papermill to handle notebook executions."""

    @classmethod
    def execute_managed_notebook(cls, nb_man, kernel_name=None, **kwargs):
        """The interface method used by papermill to initiate an execution request"""
        return run_sync(cls(nb_man, **kwargs).execute)(kernel_name=kernel_name, **kwargs)

    def __init__(
        self,
        nb_man: NotebookExecutionManager,
        km: Optional[KernelManager] = None,
        timeout_func=None,
        timeout: float = None,
        log_output: bool = False,
        stdout_file=None,
        stderr_file=None,
        **kw
    ):
        """Initializes the execution manager.

        Parameters
        ----------
        nb_man : NotebookExecutionManager
            Notebook execution manager wrapper being executed.
        km : KernerlManager (optional)
            Optional kernel manager. If none is provided, a kernel manager will
            be created.
        """
        self.nb_man = nb_man
        self.km = km
        self.timeout_func = timeout_func
        self.timeout = timeout
        self.log_output = log_output
        self.stdout_file = stdout_file
        self.stderr_file = stderr_file
        self.kernel_name = kw.get('kernel_name', '__NOT_SET__')
        self.nb = nb_man.nb

    async def execute(self, **kwargs):
        """Executes a notebook using Noteable's APIs"""
        async with self.setup_kernel(**kwargs):
            logger.info("Executing notebook with kernel: %s" % self.kernel_name)
            await self.papermill_execute_cells()
            # info_msg = self.wait_for_reply(self.kc.kernel_info())
            # self.nb.metadata['language_info'] = info_msg['content']['language_info']

        return self.nb

    def create_kernel_manager(self, file: NotebookFile, client: NoteableClient, **kwargs):
        """Helper that generates a kernel manager object from kwargs"""
        return NoteableKernelManager(file, client, **kwargs)

    @asynccontextmanager
    async def setup_kernel(self, cleanup_kc=True, cleanup_kc_on_error=False, **kwargs) -> Generator:
        """Context manager for setting up the kernel to execute a notebook."""
        if self.km is None:
            # Assumes that file and client are being passed in
            self.km = self.create_kernel_manager(**kwargs)

        # Subscribe to the file or we won't see status updates
        await self.km.client.subscribe_file(self.km.file)
        await self.km.async_start_kernel(**kwargs)
        try:
            yield
            # if cleanup_kc:
            #     if await self.km.async_is_alive():
            #         await self.km.async_shutdown_kernel()
        finally:
            pass
            # if cleanup_kc and cleanup_kc_on_error:
            #     if await self.km.async_is_alive():
            #         await self.km.async_shutdown_kernel()

    sync_execute = run_sync(execute)

    async def papermill_execute_cells(self):
        """This function replaces cell execution with its own wrapper.

        We are doing this for the following reasons:

        1. Notebooks will stop executing when they encounter a failure but not
           raise a `CellException`. This allows us to save the notebook with the
           traceback even though a `CellExecutionError` was encountered.

        2. We want to write the notebook as cells are executed. We inject our
           logic for that here.

        3. We want to include timing and execution status information with the
           metadata of each cell.
        """
        # Execute each cell and update the output in real time.
        for index, cell in enumerate(self.nb.cells):
            try:
                self.nb_man.cell_start(cell, index)
                await self.async_execute_cell(cell, index)
            except CellExecutionError as ex:
                # TODO: Make sure we raise these
                self.nb_man.cell_exception(self.nb.cells[index], cell_index=index, exception=ex)
                break
            finally:
                self.nb_man.cell_complete(self.nb.cells[index], cell_index=index)

    def _get_timeout(self, cell: Optional[NotebookNode]) -> int:
        """Helper to fetch a timeout as a value or a function to be run against a cell"""
        if self.timeout_func is not None and cell is not None:
            timeout = self.timeout_func(cell)
        else:
            timeout = self.timeout

        if not timeout or timeout < 0:
            timeout = None

        return timeout

    async def async_execute_cell(
        self, cell: NotebookNode, cell_index: int, **kwargs
    ) -> NotebookNode:
        """
        Executes a single code cell.

        To execute all cells see :meth:`execute`.

        Parameters
        ----------
        cell : nbformat.NotebookNode
            The cell which is currently being processed.
        cell_index : int
            The position of the cell within the notebook object.

        Returns
        -------
        output : dict
            The execution output payload (or None for no output).

        Raises
        ------
        CellExecutionError
            If execution failed and should raise an exception, this will be raised
            with defaults about the failure.

        Returns
        -------
        cell : NotebookNode
            The cell which was just processed.
        """
        assert self.km.client is not None
        if cell.cell_type != 'code':
            logger.debug("Skipping non-executing cell %s", cell_index)
            return cell

        logger.debug("Executing cell:\n%s", cell.id)

        # TODO: Handle
        # if self.record_timing and 'execution' not in cell['metadata']:
        #     cell['metadata']['execution'] = {}

        # TODO: Handle
        # cell_allows_errors = (not self.force_raise_errors) and (
        #     self.allow_errors
        #     or "raises-exception" in cell.metadata.get("tags", []))

        # By default this will wait until the cell execution status is no longer active
        result = await self.km.client.execute(self.km.file, cell.id)
        # TODO: This wasn't behaving correctly with the timeout?!
        # result = await asyncio.wait_for(self.km.client.execute(self.km.file, cell.id), self._get_timeout(cell))
        logger.error(result.data.state)
        logger.error(result.data.state.is_error_state)
        if result.data.state.is_error_state:
            # TODO: Add error info from stacktrace output messages
            raise CellExecutionError("", str(result.data.state), "Cell execution failed")
        return cell

    def log_output_message(self, output):
        """Process a given output. May log it in the configured logger and/or write it into
        the configured stdout/stderr files.
        """
        if output.output_type == "stream":
            content = "".join(output.text)
            if output.name == "stdout":
                if self.log_output:
                    logger.info(content)
                if self.stdout_file:
                    self.stdout_file.write(content)
                    self.stdout_file.flush()
            elif output.name == "stderr":
                if self.log_output:
                    # In case users want to redirect stderr differently, pipe to warning
                    logger.warning(content)
                if self.stderr_file:
                    self.stderr_file.write(content)
                    self.stderr_file.flush()
        elif self.log_output and ("data" in output and "text/plain" in output.data):
            logger.info("".join(output.data['text/plain']))

    def process_message(self, *arg, **kwargs):
        """Handles logging ZMQ style messages.
        TODO: Change to account for RTU outputs here?
        """
        output = super().process_message(*arg, **kwargs)
        if output and (self.log_output or self.stderr_file or self.stdout_file):
            self.log_output_message(output)
        return output

    @classmethod
    def nb_kernel_name(cls, nb, name=None):
        """
        This method is defined to override the default `Engine.nb_kernel_name` which throws an error
        when `metadata.kernelspec.name` is not present in the notebook.
        Noteable notebooks do not store `kernelspec` metadata.
        """
        return
