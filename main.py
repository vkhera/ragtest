import os
import argparse
from rag.ingest import ingest_pdfs
from rag.cli import cli_chat
from rag.web import start_web
from rag.api import start_api

def main():
    parser = argparse.ArgumentParser(description="Local RAG Application")
    parser.add_argument('--cli', action='store_true', help='Start CLI chat interface')
    parser.add_argument('--web', action='store_true', help='Start HTML chat web interface')
    parser.add_argument('--api', action='store_true', help='Start REST API interface')
    parser.add_argument('--ingest', action='store_true', help='Ingest PDFs in ./pdfs directory')
    args = parser.parse_args()

    if args.ingest:
        ingest_pdfs('pdfs')
    elif args.cli:
        cli_chat()
    elif args.web:
        start_web()
    elif args.api:
        start_api()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
