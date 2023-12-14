// Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
//
// Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

db.geonames_filtered.drop()
db.geonames.aggregate([

    // Keep only named entities that 
    // (1) are at least 3 characters long and 
    // (2) have a wikidataId field
    // (3) do not begin with non-alphabetic characters 

    { $project: {
        'paper_id': 1,

        'title.entities': { $filter: { input: "$title.entities",  cond: { $and: [
            { $ne:  ["$$this.GeoNamesID", undefined] },
            { $regexMatch: {input: "$$this.rawName", regex: "^[a-z,A-Z,À-ÿ,\p{Greek},µ]" } },
            { $gte: [{$strLenCP: "$$this.rawName"}, 2] },
            { $gte: ["$$this.confidence_score", 0.0] }
        ]}}},

        'abstract.entities': { $filter: { input: "$abstract.entities",  cond: { $and: [
            { $ne:  ["$$this.GeoNamesID", undefined] },
            { $regexMatch: {input: "$$this.rawName", regex: "^[a-z,A-Z,À-ÿ,\p{Greek},µ]" } },
            { $gte: [{$strLenCP: "$$this.rawName"}, 2] },
            { $gte: ["$$this.confidence_score", 0.0] }
        ]}}},

        'body_text.entities': { $filter: { input: "$body_text.entities",  cond: { $and: [
            { $ne:  ["$$this.GeoNamesID", undefined] },
            { $regexMatch: {input: "$$this.rawName", regex: "^[a-z,A-Z,À-ÿ,\p{Greek},µ]" } },
            { $gte: [{$strLenCP: "$$this.rawName"}, 2] },
            { $gte: ["$$this.confidence_score", 0.0] }
        ]}}},
    }},

    { $out: "geonames_filtered" }
])

db.geonames_filtered.createIndex({paper_id: 1})
