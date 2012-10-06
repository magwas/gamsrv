#!/usr/bin/python

import unittest

from persistence.enumtype import EnumType, ValidationError

from xml.dom.minidom import parseString

class TestEnumType(unittest.TestCase):

	def test_empty_toDom(self):
		t1 = EnumType("test:enumtype:empty", cleanup = True, incremental = True)
		self.assertEqual(t1.toDom().toxml(),'<enum name="test:enumtype:empty"/>')
		t1.registerOne("one")
		self.assertEqual(t1.toDom().toxml(),'<enum name="test:enumtype:empty"><value id="0" name="one"/></enum>')

	def test_enum_1(self):
		t2 = EnumType("test:enumtype:enum",enum=('one','three','two'))
		n = parseString('<enum name="test:enumtype:enum"><value id="0" name="one"/><value id="1" name="three"/><value id="2" name="two"/></enum>').childNodes[0]
		self.assertEqual(t2.toDom().toxml(),n.toxml())

		self.assertEqual(t2.stringFor(0),'one')
		self.assertEqual(t2.intFor('one'),0)
		self.assertEqual(t2.valueList(),[0,1,2])
		self.assertTrue(t2.validate(0))
		self.assertTrue(t2.validate(1))
		self.assertTrue(t2.validate(2))
		self.assertRaises(ValidationError,t2.validate,-1)

	def test_enum_2(self):
		t3 = EnumType("test:enumtype:valuedenum",enumdict={42:'Three', -1:'One', 22:'Two'})
		n3 = parseString('<enum name="test:enumtype:valuedenum"><value id="-1" name="One"/><value id="22" name="Two"/><value id="42" name="Three"/></enum>').childNodes[0]
		self.assertEqual(t3.toDom().toxml(),n3.toxml())
		self.assertTrue(t3.validate(-1))
		self.assertTrue(t3.validate(42))
		self.assertTrue(t3.validate(22))
		self.assertEqual(t3.valueList(),[-1,22,42])
		self.assertRaises(ValueError,t3.stringFor,1)
		self.assertEqual(t3.stringFor(-1),'One')
		self.assertEqual(t3.intFor('Two'),22)
		self.assertRaises(ValidationError,t3.validate,1)

		t4 = EnumType("test:enumtype:valuedenum")
		self.assertEqual(t3.toDom().toxml(),t4.toDom().toxml())
		self.assertTrue(t4.validate(-1))
		self.assertTrue(t4.validate(42))
		self.assertTrue(t4.validate(22))
		self.assertEqual(t4.valueList(),[-1,22,42])
		self.assertRaises(ValueError,t4.stringFor,1)
		self.assertEqual(t4.stringFor(-1),'One')
		self.assertEqual(t4.intFor('Two'),22)
		self.assertRaises(ValidationError,t4.validate,1)
		EnumType("test:enumtype:enum",enum=('one','three','two'))

	def test_enum_3(self):
		t5 = EnumType("test:enumtype:incremental",enumdict={42:'Three', -1:'One', 22:'Two'},incremental=True)
		t5.registerOne('The only one', 1)
		t5.registerOne('The only two')
		with self.assertRaises(ValueError):
			t5.registerOne('THe only one', 1)
		t5.finalize()
		t5.persist()
		t6 = EnumType("test:enumtype:incremental")
		self.assertEqual(t5.toDom().toxml(),t5.toDom().toxml())

		with self.assertRaises(ValueError):
			t5.registerOne('Tiii')
		n5 = parseString('<enum name="test:enumtype:incremental"><value id="-1" name="One"/><value id="1" name="The only one"/><value id="22" name="Two"/><value id="42" name="Three"/><value id="43" name="The only two"/></enum>').childNodes[0]
		self.assertEqual(t5.toDom().toxml(),n5.toxml())

		with self.assertRaises(ValueError):
			t5.registerOne(1,'The only one')

		
		with self.assertRaises(ValueError):
			EnumType("test:enumtype:enum",enum=('one','thRee','two'))
			EnumType("test:enumtype:valuedenum",enumdict={42:'ThRee', -1:'One', 22:'Two'})
			EnumType("test:enumtype:otherenum",enumdict={'ThRee':42, 'One':-1, 'Two': 22})

		

	def tearDown(self):
		return
		EnumType("test:enumtype:enum")._unpersist()
		EnumType("test:enumtype:valuedenum")._unpersist()

if __name__ == '__main__':
	unittest.main()

