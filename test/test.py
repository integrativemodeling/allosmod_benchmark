#!/usr/bin/env python

import unittest
import os
import sys
import subprocess
import glob
import shutil

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
        subprocess.check_call(['/bin/sh', './qsub.sh'])
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

if __name__ == '__main__':
    unittest.main()
