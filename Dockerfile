FROM python:3.7.7

ENV HOMEDIR /home/appuser
RUN useradd --create-home appuser

# install python deps
RUN pip install \
		htmlement==1.0 \ 
		requests==2.24.0 \
		biopython==1.77



COPY src/gor1_server.py /usr/local/bin/
COPY src/multi_fasta_exec.py /usr/local/bin/
RUN chmod -R a+rx /usr/local/bin

USER appuser
WORKDIR ${HOMEDIR}

ENTRYPOINT ["bash"]
