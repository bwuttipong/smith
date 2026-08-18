// ============================================================
// C# Interview Question - Top 5 Coding Questions #4
// "Write a C# program to find if a positive integer is prime or not"
// Source: SimplyLearn - C# Interview Questions and Answers
// ============================================================

using System;

namespace CSharpInterview
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Enter a positive integer to check if it's prime:");
            string input = Console.ReadLine();

            if (int.TryParse(input, out int number) && number > 0)
            {
                if (IsPrime(number))
                    Console.WriteLine($"{number} is a prime number.");
                else
                    Console.WriteLine($"{number} is not a prime number.");
            }
            else
            {
                Console.WriteLine("Please enter a valid positive integer.");
            }
        }

        static bool IsPrime(int number)
        {
            if (number <= 1) return false;
            if (number == 2) return true;       // 2 is the only even prime
            if (number % 2 == 0) return false;  // other even numbers are not prime

            // Check odd divisors up to square root
            int limit = (int)Math.Sqrt(number);
            for (int i = 3; i <= limit; i += 2)
            {
                if (number % i == 0)
                    return false;
            }
            return true;
        }
    }
}