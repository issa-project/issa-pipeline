// Author: Anna BOBASHEVA, University Cote d'Azur, Inria
// Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

// Collection of thematic decriptors from metadata
// where the descriptors are being stored as an array    
db.document_descriptors.drop()
db.document_metadata.aggregate([
  { $project : { descriptor_uri : { $split: ["$descriptors_uris", ", "] }, paper_id : 1, _id: 0 } },
  { $unwind : "$descriptor_uri" },
  { $project : { descriptor_uri: { $trim: { input: "$descriptor_uri", chars: "'[]" }  }, paper_id : 1, _id: 0 } },
  { $match : { descriptor_uri : {$ne: ""} } },
  { $out: "document_descriptors" }
])
db.document_descriptors.createIndex({paper_id: 1})
db.document_descriptors.count()
