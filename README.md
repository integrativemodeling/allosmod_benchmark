This benchmark tests the AllosMod method, as implemented in the
[AllosMod library](https://github.com/salilab/allosmod-lib) and
[AllosMod web service](http://salilab.org/allosmod).

## Benchmark files

- `3UWPA`: basic test of the method
- `input_glyc`: test of the support for glycosylation

To run the benchmark, first [install AllosMod and its dependencies](https://allosmod.readthedocs.org/en/latest/installation.html).
Then, in each directory, run `allosmod setup` to check the input files; this
will generate a file `qsub.sh`. Run this script to set up the system. In the
`3UWPA` case, this is in turn will generate input files for
[MODELLER](http://salilab.org/modeller/) which should be run with that program.

## Information

_Author(s)_: Patrick Weinkam, Ben Webb

_License_: [LGPL](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html).
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.

_Last known good IMP version_: [![build info](https://integrativemodeling.org/systems/?sysstat=16&branch=master)](http://integrativemodeling.org/systems/) [![build info](https://integrativemodeling.org/systems/?sysstat=16&branch=develop)](http://integrativemodeling.org/systems/)

_Testable_: Yes.

_Parallelizeable_: Yes

_Publications_:
 - [Weinkam P, Pons J, Sali A., Proc Natl Acad Sci USA. (2012) 109, 4875-80.](http://www.ncbi.nlm.nih.gov/pubmed/22403063)
 - [Guttman M, Weinkam P, Sali A, Lee KK, Structure (2013) 21, 321-31.](http://www.ncbi.nlm.nih.gov/pubmed/23473666)
