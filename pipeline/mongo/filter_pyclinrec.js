// Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
//
// Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

db.pyclinrec_filtered.drop()
db.pyclinrec.aggregate([

    // Keep only named entities:
    // (1) with a URI (should be all of them)
    // (2) with a similarityScore higher than 0.75
    // (3) that are at least 3 characters long
    { $project: {
        paper_id: 1,

        'title.concepts': { $filter: { input: "$title.concepts",  cond: { $and: [
            { $ne: ["$$this.concept_id", undefined] },
            { $gte: ["$$this.confidence_score", 0.75] },
            { $regexMatch: {input: "$$this.matched_text", regex: "^[a-z,A-Z,À-ÿ,\p{Greek},µ]" } },
            { $gte: [{$strLenCP: { $convert: { input: "$$this.matched_text", to: "string"}}}, 3] }
        ]}}},

        
        'abstract.concepts': { $filter: { input: "$abstract.concepts",  cond: { $and: [
            { $ne: ["$$this.concept_id", undefined] },
            { $gte: ["$$this.confidence_score", 0.75] },
            { $regexMatch: {input: "$$this.matched_text", regex: "^[a-z,A-Z,À-ÿ,\p{Greek},µ]" } },
            { $gte: [{$strLenCP: { $convert: { input: "$$this.matched_text", to: "string"}}}, 3] }
        ]}}},

        'body_text.concepts': { $filter: { input: "$body_text.concepts",  cond: { $and: [
            { $ne: ["$$this.concept_id", undefined] },
            { $gte: ["$$this.confidence_score", 0.75] },
            { $regexMatch: {input: "$$this.matched_text", regex: "^[a-z,A-Z,À-ÿ,\p{Greek},µ]" } },
            { $gte: [{$strLenCP: { $convert: { input: "$$this.matched_text", to: "string"}}}, 3] }
        ]}}}


    }},


    { $out: "pyclinrec_filtered" }
])

db.pyclinrec_filtered.createIndex({paper_id: 1})
