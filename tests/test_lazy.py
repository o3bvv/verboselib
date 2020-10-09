import unittest

from verboselib.lazy import LazyString


class LazyStringTestCase(unittest.TestCase):

  def test_str(self):
    testee = LazyString(lambda: "foo")
    self.assertEqual(str(testee), "foo")

  def test_args_kwargs(self):
    testee = LazyString(
      lambda a, b: "{} =? {} : {}".format(a, b, a == b),
      10,
      b=20
    )
    self.assertEqual(testee, "10 =? 20 : False")

  def test_format(self):
    testee = LazyString(lambda: "name: {name}")
    self.assertEqual(testee.format(name="foo"), "name: foo")

  def test_invalid_attribute(self):
    testee = LazyString(lambda: "foo")

    with self.assertRaises(AttributeError):
      testee.foo()

  def test_len(self):
    testee = LazyString(lambda: "foo")
    self.assertEqual(len(testee), 3)

  def test_indexing(self):
    testee = LazyString(lambda: "foo")
    self.assertEqual(testee[0], "f")

  def test_iter(self):
    testee = LazyString(lambda: "foo")
    self.assertEqual(list(iter(testee)), ["f", "o", "o"])

  def test_contains(self):
    testee = LazyString(lambda: "foo")
    self.assertIn("f", testee)

  def test_add(self):
    testee = LazyString(lambda: "foo")
    self.assertEqual(testee + "bar", "foobar")

  def test_radd(self):
    testee = LazyString(lambda: "foo")
    self.assertEqual("bar" + testee, "barfoo")

  def test_mul(self):
    testee = LazyString(lambda: "foo")
    self.assertEqual(testee * 3, "foofoofoo")

  def test_rmul(self):
    testee = LazyString(lambda: "foo")
    self.assertEqual(3 * testee, "foofoofoo")

  def test_eq(self):
    testee = LazyString(lambda: "foo")
    self.assertEqual(testee, "foo")

  def test_ne(self):
    testee = LazyString(lambda: "foo")
    self.assertNotEqual(testee, "bar")

  def test_lt(self):
    testee = LazyString(lambda: "foo")
    self.assertFalse(testee < "boo")
    self.assertTrue( testee < "joo")

  def test_le(self):
    testee = LazyString(lambda: "foo")
    self.assertFalse(testee <= "boo")
    self.assertTrue( testee <= "foo")
    self.assertTrue( testee <= "joo")

  def test_gt(self):
    testee = LazyString(lambda: "foo")
    self.assertTrue( testee > "boo")
    self.assertFalse(testee > "joo")

  def test_ge(self):
    testee = LazyString(lambda: "foo")
    self.assertTrue( testee >= "boo")
    self.assertTrue( testee >= "foo")
    self.assertFalse(testee >= "joo")
