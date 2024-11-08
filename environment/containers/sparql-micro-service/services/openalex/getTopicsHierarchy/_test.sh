#!/bin/bash

Q='prefix%20dct%3A%20%20%20%20%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Felements%2F1.1%2F%3E%0Aprefix%20skos%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0Aconstruct%20where%20%7B%0A%20%3Fs%20%3Fp%20%3FO.%0A%7D'
 
curl -v --header "accept: text/turtle" "http://localhost/service/openalex/getTopicsHierarchy?query=$Q&page=1&per_page=1"
