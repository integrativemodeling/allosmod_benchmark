#!/usr/bin/env python

import unittest
import os
import sys
import subprocess
import glob
import shutil
import modeller

# Remove SGE-specific environment variables, so AllosMod script thinks it's
# running outside of SGE
for e in ['JOB_ID', 'SGE_TASK_ID']:
    if e in os.environ:
        del os.environ[e]

TOPDIR = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))

class Tests(unittest.TestCase):
    def test_3UWPA(self):
        """Test 3UWPA benchmark (regular AllosMod)"""
        os.chdir(os.path.join(TOPDIR, 'benchmark', '3UWPA'))
        # Cleanup anything left over from a previous run
        shutil.rmtree('pred_dECALCrAS1000', ignore_errors=True)

        subprocess.check_call(['allosmod', 'setup'])
        # Setup should generate ligand and script:
        for f in ['lig.pdb', 'qsub.sh']:
            self.assertTrue(os.path.exists(f))
        # Run the protocol
        subprocess.check_call(['/bin/sh', '--login', './qsub.sh'])
        # Should generate more files:
        for f in ['README', 'pred_dECALCrAS1000/3UWP.pdb_0']:
            self.assertTrue(os.path.exists(f))
        for f in ['model_run.py', 'random.ini', 'align.ali', 'converted.rsr',
                  '3UWP.pdb', 'allosmod.py']:
            self.assertTrue(os.path.exists(os.path.join(
                                    'pred_dECALCrAS1000', '3UWP.pdb_0', f)))

        os.chdir('pred_dECALCrAS1000/3UWP.pdb_0')
        # Skip the actual MD optimization to make the sampling faster
        with open('model_run.py') as fh:
            contents = fh.read()
        with open('model_run.py', 'w') as fh:
            fh.write("def dummy_opt(*args, **keys): pass\n")
            fh.write("from modeller.optimizers import molecular_dynamics\n")
            fh.write("molecular_dynamics.optimize = dummy_opt\n\n")
            fh.write(contents)
        # Run the sampling
        subprocess.check_call(['python', 'model_run.py'])
        # Should have generated a set of PDB files:
        for i in range(17) + range(501, 511) + range(1001, 3001):
            os.unlink('pm.pdb.B%04d0001.pdb' % i)
        self.assertEqual(glob.glob('pm.pdb.B*.pdb'), ['pm.pdb.B99990001.pdb'])
        for f in ['pm.pdb.ini', 'pm.pdb.sch', 'pm.pdb.V99990001',
                  'pm.pdb.D00000001']:
            self.assertTrue(os.path.exists(f))
        # todo: test the analysis scripts

    def test_glyc(self):
        """Test glycosylation benchmark"""
        os.chdir(os.path.join(TOPDIR, 'benchmark', 'input_glyc'))
        # Cleanup anything left over from a previous run
        shutil.rmtree('pred_dECALCrAS1000', ignore_errors=True)

        subprocess.check_call(['allosmod', 'setup'])
        # Setup should generate ligand and script:
        for f in ['lig.pdb', 'qsub.sh']:
            self.assertTrue(os.path.exists(f))
        # Run the protocol
        subprocess.check_call(['/bin/sh', '--login', './qsub.sh'])
        # Should generate more files:
        os.chdir('pred_dECALCrAS1000/2AAS.pdb_0')
        for f in ['align2.ali', 'allosmod.py', 'converted.rsr',
                  'model_glyc.log', 'model_glyc.py', 'pm.pdb.B99990001.pdb',
                  'pm.pdb.D00000001', 'pm.pdb.V99990001', 'run.log']:
            self.assertTrue(os.path.exists(f))

        # Generated model should have sugars added to second chain
        e = modeller.environ()
        e.io.hetatm = True
        m = modeller.model(e, file='pm.pdb.B99990001.pdb')
        self.assertEqual(len(m.chains), 2)
        self.assertEqual(len(m.chains[0].residues), 124)
        self.assertEqual(len(m.chains[1].residues), 16)
        self.assertEqual([r.name for r in m.chains[1].residues],
                         ['NAG', 'NAG', 'BMA', 'MAN', 'MAN', 'MAN', 'MAN',
                          'MAN', 'NAG', 'NAG', 'BMA', 'MAN', 'MAN', 'MAN',
                          'MAN', 'MAN'])

if __name__ == '__main__':
    unittest.main()
