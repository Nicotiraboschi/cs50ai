import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}: ")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}: ")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p: .4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    no_genes = {person for person in people if person not in one_gene and person not in two_genes}
    
    def find_parents(person):
        mother = people[person]["mother"]
        father = people[person]["father"]
        return mother, father
    
    joint_prob = {}
    
    genes_dict = {}
    
    for person in one_gene:
        genes_dict[person] = 1
    for person in two_genes:
        genes_dict[person] = 2
    for person in no_genes:
        genes_dict[person] = 0    
    
    for person in genes_dict:
        number = genes_dict[person]
        person_have_trait = True if person in have_trait else False    
        mother, father = find_parents(person)
        prob_2 = PROBS["trait"][number][person_have_trait]
        if not mother:
            prob_1 = PROBS["gene"][number]
            person_have_trait = True if person in have_trait else False
            
            prob_combined = prob_1 * prob_2
            joint_prob[person] = prob_combined
        else:
            def calc_parent(parent):
                direct_gene = 1 if parent in two_genes else (0.5 if parent in one_gene else 0)
                mut_probs = PROBS["mutation"]
                direct_gene += mut_probs if direct_gene == 0 else (-mut_probs if direct_gene == 1 else 0)
                
                print(direct_gene, "direct")
                return direct_gene
            
            from_mother = calc_parent(mother)
            from_father = calc_parent(father)
            
            if number == 1:
                prob_combined = from_mother * (1-from_father) + from_father * (1-from_mother)
            elif number == 2:   
                prob_combined = from_mother * from_father
            else:
                prob_combined = (1-from_mother) * (1-from_father)

            joint_prob[person] = prob_combined * prob_2

    p = 1
    for value in joint_prob.values():
        p *= value
    return p


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    print(p)
        
    for person in probabilities.keys():
        number = 1 if person in one_gene else (2 if person in two_genes else 0)
        update_gene = probabilities[person]["gene"][number]
        if not update_gene:
            update_gene = p
        else:
            update_gene += p
        trait = True if person in have_trait else False
        update_trait = probabilities[person]["trait"][trait]
        if not update_trait:
            update_trait = p
        else:
            update_trait += p
        probabilities[person]["gene"][number] = update_gene
        probabilities[person]["trait"][trait] = update_trait


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    for person in probabilities:
        sum_probs_genes = 0
        sum_probs_traits = 0
        for value in probabilities[person]["gene"].values():
            sum_probs_genes += value
        print(sum_probs_genes, "after")
        for value in probabilities[person]["trait"].values():
            sum_probs_traits += value
        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] /= sum_probs_genes
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= sum_probs_traits


if __name__ == "__main__":
    main()
