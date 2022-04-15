// Author: Anna BOBASHEVA, University Cote d'Azur, Inria
// Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

// Collection of thematic decriptors from metadata
// where the descriptors are being stored as an array    
db.document_descriptors.drop()
db.document_metadata.aggregate([
  { $project : { agrovoc_uri : { $split: ["$agrovoc_uris", ", "] }, agritrop_id : 1, _id: 0 } },
  { $unwind : "$agrovoc_uri" },
  { $project : { agrovoc_uri: { $trim: { input: "$agrovoc_uri", chars: "'[]" }  }, agritrop_id : 1, _id: 0 } },
  { $match : { agrovoc_uri : {$ne: ""} } },
  { $out: "document_descriptors" }
])
db.document_descriptors.createIndex({agritrop_id: 1})
db.document_descriptors.count()
