// Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
//
// Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

// Extract document thematic descriptors from the metadata where they are saved as strings
// and save them in a separate collection for RDF transformation by xR2RML

db.document_descriptors.drop()
db.document_metadata.aggregate([
     // Remove brackets 
	{ $project : { uris:   { $trim: { input: "$descriptors_uris", chars: "[]" }  },
                    labels: { $trim: { input: "$descriptors_labels", chars: "[]\"" }  },
                    paper_id : 1, _id: 1, iso_lang: 1 } 
	},

     // Split strings into arrays
	{ $project : { uris :   { $split: ["$uris", ", "] },
                    labels : { $split: ["$labels", ", "] },
                    paper_id : 1, _id: 1 , iso_lang: 1} },

     // Remove extra quotes	 
	{ $project : { uris :   { $map : { input: "$uris",   as : "uri", in: { $trim: {input : "$$uri", chars: "'\""} }}},
                    labels : { $map : { input: "$labels", as : "lbl", in: { $trim: {input : "$$lbl", chars: "'\""} }}},
				cnt :    { $size:  "$uris" },
                    paper_id : 1, _id: 1 , iso_lang: 1} },

     // Take only documents with existing descriptors
	{ $match : { uris : {$ne: [""]} } },

     // Zip descriptors URIs and labels and save them as objects
	{ $project : { subjects : {$map : {
	                             input: { $zip : {inputs : [ "$uris", "$labels" , {$range : [1, {$add : ["$cnt", 1]} ] } ] } },
						    as : "descr",
						    in : { uri :    { $arrayElemAt: [ "$$descr", 0 ] }, 
	                                    label :  { $arrayElemAt: [ "$$descr", 1 ] }, 
								 rank  :  { $arrayElemAt: [ "$$descr", 2 ] } }
                                  } } ,
                 paper_id : 1, _id: 1 , iso_lang: 1, cnt: 1} },
  // Save output to a new collection
  { $out: "document_descriptors" }
])

db.document_descriptors.createIndex({paper_id: 1})
db.document_descriptors.count()


// Extract document domains from the metadata where they are saved as strings
// and save them in a separate collection for RDF transformation by xR2RML

//TODO: change the input field for labels

db.document_domains.drop()
db.document_metadata.aggregate([
     // Remove brackets 
	{ $project : { uris:   { $trim: { input: "$domain_codes", chars: "[]" }  },
                    labels: { $trim: { input: "$domain_codes", chars: "[]\"" }  },
                    paper_id : 1, _id: 1} 
	},

     // Split strings into arrays
	{ $project : { uris :   { $split: ["$uris", ", "] },
                    labels : { $split: ["$labels", ", "] },
                    paper_id : 1, _id: 1} },

     // Remove extra quotes	 
	{ $project : { uris :   { $map : { input: "$uris",   as : "uri", in: { $trim: {input : "$$uri", chars: "'\""} }}},
                   labels : { $map : { input: "$labels", as : "lbl", in: { $trim: {input : "$$lbl", chars: "'\""} }}},
				cnt :    { $size:  "$uris" },
                    paper_id : 1, _id: 1 } },

     // Take only documents with existing domains
	{ $match : { uris : {$ne: [""]} } },

     // Zip domains URIs and labels and save them as objects
	{ $project : { subjects : {$map : {
	                             input: { $zip : {inputs : [ "$uris", "$labels" , {$range : [1, {$add : ["$cnt", 1]} ] } ] } },
						    as : "descr",
						    in : { uri :   { $arrayElemAt: [ "$$descr", 0 ] }, 
	                                 label :  { $arrayElemAt: [ "$$descr", 1 ] }, 
								 rank  :  { $arrayElemAt: [ "$$descr", 2 ] } }
                                  } } ,
                 paper_id : 1, _id: 1 , cnt: 1} },
  // Save output to a new collection
  { $out: "document_domains" }
])

db.document_domains.createIndex({paper_id: 1})
db.document_domains.count()
