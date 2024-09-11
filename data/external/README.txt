Network data for the paper "Dimension-reduction of dynamics on real-world networks with symmetry". This includes, for each network:

(i) network data in a format readable by the sparse graph automorphism generator code saucy (http://vlsicad.eecs.umich.edu/BK/\
SAUCY/)
(ii) output from the sparse graph automorphism generator code
(iii) GAP (https://www.gap-system.org) readable information derived from the saucy output 
(iv) csv file containing number of orbits representatives (i.e. |S/G| for binary state-space S and automorphism group G)

This data can be used to identify real-world networks with significant lumping, i.e. cases where network symmetries facilitate the exact mathematical analysi of dynamical processes (specifically binary state-space single-vertex-transition models) on those networks.

The networks were originally downloaded from http://networkrepository.com, licensed under a Creative Commons Attribution-ShareAlike License.


Descriptions of each zip file:


(i)
dataset title: networkrepositorydata_scy_202021001.zip
creator: Jonathan Ward
dataset description: Network data in saucy readabe format

This zip file contains a folder with networks in a format readable by the sparse graph automorphism generator code saucy. Self edges and isolated nodes were removed and edges were made undirected and unweighted before the networks were written in saucy format. The saucy format has a header with the number of nodes, number of edges and number of colours (here number of colours is always 1). The remainder of the file consists of pairs of vertex ids (starting from zero) that indicate the presence of an edge. Vertex ids may differ from those in the original networkrepository data. 


(ii)
dataset title: networkrepositorydata_scyoutput_202021001.zip
creator: Jonathan Ward
dataset description: Saucy output

This zip file contains a folder with the output from the sparse graph automorphism generator code saucy. For each network there is a .gaut file and a .log file. The .gaut file contains graph automorphism generators written in cycle notation (and is empty if the network has no symmetries). The .log file contains log information output from saucy (see http://vlsicad.eecs.umich.edu/BK/SAUCY/ for details).


(iii)
dataset title: networkrepositorydata_gapinput_202021001.zip
creator: Jonathan Ward
dataset description: GAP readable network autormorphism data

This zip file contains a folder with a file of GAP readable information derived from the saucy. For each network there is a .gap file that defines the number of vertices in the network, the network automorphism group generators z and the automorphism group g.


(iv)
dataset title: networkrepositorydata_orbitrepresentativeinfo_202021001.csv
creator: Jonathan Ward
dataset description: csv file of network data

The fields in this csv file are:
 : row number (starting from zero)
name : name of network - this corresponds to the files in networkrepositorydata_scy_202021001.zip, networkrepositorydata_scyoutput_202021001.zip and networkrepositorydata_gapinput_202021001.zip
Type : Network type as listed in networkrepository.com (at time of download)
N : Number of vertices
M : Number of edges
NrMoved : Number of vertices moved by at least one permutation
OtherSD : Description of the type of symmetry (BSM: Basic symmetric motif; otherwise includes output from GAP function StructureDescription, where possible)
nORsMPs : Number of orbits of the moved points (computed using methods described in paper above)
nORsMPsPE : Number of orbits of the moved points (computed using Polya enumeration)
