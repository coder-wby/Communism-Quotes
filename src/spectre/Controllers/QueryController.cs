using System;
using System.Collections.Generic;
using System.Text.Json;
using Microsoft.AspNetCore.Mvc;

namespace spectre.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class QueryController : ControllerBase
    {
        [HttpPost]
        public IEnumerable<string> Query([FromBody] JsonElement qry)
        {
            // qry是一个json
            foreach (var prop in qry.EnumerateObject())
                Console.WriteLine($"{prop.Name} = {prop.Value}");

            var ret = new List<string> {$"result for {qry}:"};
            for (int i = 0; i < 10; i++)
                ret.Add($"result {i + 1}");
            ret.Add($" 以上是关键字[{qry}]搜索的结果");

            return ret;
        }
    }
}