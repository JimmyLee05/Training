using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace WelcomeYou
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("use continue to quit circular：");
            for (int i=0; i<5; i++)
            {
                if (i==2)
                {
                    continue;
                }

                Console.WriteLine("now i is：{0}", i);
            }

            Console.WriteLine("use break to quit");
            for (int i=0; i<5; i++)
            {
                if (i==2)
                {
                    break;
                }

                Console.WriteLine("now the i is：{0}", i);
            }

            Console.Read();
        }
    }
}


