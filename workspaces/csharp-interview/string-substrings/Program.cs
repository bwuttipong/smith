// ============================================================
// C# Interview Question - Top 5 Coding Questions #3
// "Write a C# program to find the substring from a given string"
// Source: SimplyLearn - C# Interview Questions and Answers
// ============================================================

using System;

namespace CSharpInterview
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Enter a string:");
            string input = Console.ReadLine();

            Console.WriteLine("\nAll possible substrings:");
            PrintAllSubstrings(input);
        }

        static void PrintAllSubstrings(string input)
        {
            int length = input.Length;
            int count = 0;

            for (int i = 0; i < length; i++)
            {
                for (int j = i + 1; j <= length; j++)
                {
                    string substring = input.Substring(i, j - i);
                    Console.WriteLine($"[{count++}] \"{substring}\" (start={i}, length={j - i})");
                }
            }

            Console.WriteLine($"\nTotal substrings: {count}");
        }
    }
}