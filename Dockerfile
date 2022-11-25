# FROM elyra/elyra:2.2.4
FROM python:3.10.1

RUN python -m pip install --upgrade pip
# RUN pip install nbresuse xeus-python nbconvert matplotlib tensorflow-gpu
# RUN pip install nbresuse xeus-python nbconvert pandas matplotlib && \
#     pip install jupyterlab_latex jupyterlab-python-file lckr-jupyterlab-variableinspector && \
#     pip install jupyterlab_code_formatter jupyterlab-spreadsheet-editor ipympl
RUN pip install jupyter -U && pip install jupyterlab isort black && \
    pip install nbresuse xeus-python nbconvert pandas matplotlib && \
    pip install jupyterlab_latex jupyterlab-python-file lckr-jupyterlab-variableinspector && \
    pip install jupyterlab_code_formatter jupyterlab-spreadsheet-editor ipympl

# ---------------------
# RUN python -m pip install --upgrade pip
# RUN pip install jupyter -U && pip install jupyterlab isort black && \
#     pip install nbresuse xeus-python nbconvert pandas matplotlib && \
#     pip install jupyterlab_latex jupyterlab-python-file lckr-jupyterlab-variableinspector && \
#     pip install jupyterlab_code_formatter jupyterlab-spreadsheet-editor ipympl && \
# ---------------------

# RUN pip install jupyter_bokeh bqplot
# RUN pip install "jupyterlab-kite>=2.0.2"

# RUN rm -rf /var/lib/apt/lists/*
# COPY ./jupyter_lab_config.py /home/jovyan/.jupyter/jupyter_lab_config.py
# COPY ./jupyter_lab_config.py /home/jovyan/.jupyter/jupyter_notebook_config.py
# COPY ./jupyter_lab_config.py /home/jovyan/.ipython/profile_default/ipython_config.py
# RUN cat /home/jovyan/.jupyter/jupyter_lab_config.py
# RUN pkill jupyter-lab
# CMD ["/usr/local/bin/start-elyra.sh", "--config=/home/jovyan/.jupyter/jupyter_lab_config.py"]
# ENTRYPOINT ["jupyter", "lab", "--port=8888", "--ip=0.0.0.0", "--config=/home/jovyan/.jupyter/jupyter_lab_config.py"]
EXPOSE 8080

ENTRYPOINT ["jupyter", "lab","--port=8080", "--ip=0.0.0.0","--allow-root"]