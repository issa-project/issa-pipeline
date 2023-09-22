// Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
//
// Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

db.entityfishing_filtered.drop()
db.entityfishing.aggregate([

    // Remove unneeded fields
    { $project: {
        'title.global_categories.weight': 0,
        'title.global_categories.source': 0,
        'title.entities.nerd_selection_score': 0,
        'title.entities.wikipediaExternalRef': 0,

        'abstract.global_categories.weight': 0,
        'abstract.global_categories.source': 0,
        'abstract.entities.nerd_selection_score': 0,
        'abstract.entities.wikipediaExternalRef': 0,
        
        'body_text.global_categories.weight': 0,
        'body_text.global_categories.source': 0,
        'body_text.entities.nerd_selection_score': 0,
        'body_text.entities.wikipediaExternalRef': 0,
        }
    },

    // Keep only named entities that 
    // (1) are at least 3 characters long and 
    // (2) have a wikidataId field
    // (3) do not begin with non-alphabetic characters 

    { $project: {
        'paper_id': 1,

        'title.entities': { $filter: { input: "$title.entities",  cond: { $and: [
            { $ne:  ["$$this.wikidataId", undefined] },
            { $regexMatch: {input: "$$this.rawName", regex: "^[a-z,A-Z,À-ÿ,\p{Greek},µ]" } },
            { $gte: [{$strLenCP: "$$this.rawName"}, 3] },
            { $gte: ["$$this.confidence_score", 0.0] }
        ]}}},
        'title.global_categories': 1,

        'abstract.entities': { $filter: { input: "$abstract.entities",  cond: { $and: [
            { $ne:  ["$$this.wikidataId", undefined] },
            { $regexMatch: {input: "$$this.rawName", regex: "^[a-z,A-Z,À-ÿ,\p{Greek},µ]" } },
            { $gte: [{$strLenCP: "$$this.rawName"}, 3] },
            { $gte: ["$$this.confidence_score", 0.0] }
        ]}}},
        'abstract.global_categories': 1,

        'body_text.entities': { $filter: { input: "$body_text.entities",  cond: { $and: [
            { $ne:  ["$$this.wikidataId", undefined] },
            { $regexMatch: {input: "$$this.rawName", regex: "^[a-z,A-Z,À-ÿ,\p{Greek},µ]" } },
            { $gte: [{$strLenCP: "$$this.rawName"}, 3] },
            { $gte: ["$$this.confidence_score", 0.0] }
        ]}}},
        'body_text.global_categories': 1,
    }},

    { $out: "entityfishing_filtered" }
])

db.entityfishing_filtered.createIndex({paper_id: 1})
