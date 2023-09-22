// Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
//
// Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

db.spotlight_filtered.drop()
db.spotlight.aggregate([

    // Remove un-needed fields
    { $project: {
        'title.Resources.percentageOfSecondRank': 0,
        'title.Resources.support': 0,
        'abstract.Resources.percentageOfSecondRank': 0,
        'abstract.Resources.support': 0,
        'body_text.Resources.percentageOfSecondRank': 0,
        'body_text.Resources.support': 0
        }
    },

    // Keep only named entities:
    // (1) with a URI (should be all of them)
    // (2) with a similarityScore higher than 0.75
    // (3) that are at least 3 characters long
    { $project: {
        paper_id: 1,

        'title.Resources': { $filter: { input: "$title.Resources",  cond: { $and: [
            { $ne: ["$$this.URI", undefined] },
            { $gte: ["$$this.similarityScore", 0.75] },
            { $regexMatch: {input: { $convert: { input: "$$this.surfaceForm", to: "string"}}, regex: "^[a-z,A-Z,À-ÿ,\p{Greek},µ]" } },
            { $gte: [{$strLenCP: { $convert: { input: "$$this.surfaceForm", to: "string"}}}, 3] },
            { $eq: ["$$this.overlap", undefined] }

        ]}}},
        
        'abstract.Resources': { $filter: { input: "$abstract.Resources",  cond: { $and: [
            { $ne: ["$$this.URI", undefined] },
            { $gte: ["$$this.similarityScore", 0.75] },
	       { $regexMatch: {input: { $convert: { input: "$$this.surfaceForm", to: "string"}}, regex: "^[a-z,A-Z,À-ÿ,\p{Greek},µ]" } },
            { $gte: [{$strLenCP: { $convert: { input: "$$this.surfaceForm", to: "string"}}}, 3] },
            { $eq: ["$$this.overlap", undefined] }

        ]}}},

        'body_text.Resources': { $filter: { input: "$body_text.Resources",  cond: { $and: [
            { $ne: ["$$this.URI", undefined] },
            { $gte: ["$$this.similarityScore", 0.75] },
            { $regexMatch: {input: { $convert: { input: "$$this.surfaceForm", to: "string"}}, regex: "^[a-z,A-Z,À-ÿ,\p{Greek},µ]" } },
            { $gte: [{$strLenCP: { $convert: { input: "$$this.surfaceForm", to: "string"}}}, 3] },
            { $eq: ["$$this.overlap", undefined] }

        ]}}}


    }},

    { $out: "spotlight_filtered" }
])

db.spotlight_filtered.createIndex({paper_id: 1})
